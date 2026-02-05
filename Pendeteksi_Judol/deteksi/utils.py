from django.http import HttpResponse
from django.core.cache import cache
from django.conf import settings
import uuid
from google.oauth2.credentials import Credentials

from .services.orchestrator import analyze_content
from .services.youtube import fetch_youtube_user_info_oauth

def extract_analysis_params(request):
    """
    Mengekstrak parameter analisis dari request POST.
    
    Args:
        request: Objek HTTP request Django.
        
    Returns:
        tuple: Tuple berisi (url, selected_limit, limit, video_count, comments_per_video).
    """
    url = (request.POST.get("url") or "").strip()
    selected_limit = (request.POST.get("limit") or "")
    
    try:
        limit = int(selected_limit)
    except (ValueError, TypeError):
        limit = 100
    
    if limit == 0:
        if not request.session.get("yt_creds"):
             limit = 100 

    try:
        video_count = int(request.POST.get("video_count") or 5)
    except (ValueError, TypeError):
        video_count = 5
        
    try:
        comments_per_video = int(request.POST.get("comments_per_video") or limit)
    except (ValueError, TypeError):
        comments_per_video = limit
        
    return url, selected_limit, limit, video_count, comments_per_video

def render_htmx_inline_error(error_msg):
    """
    Mengembalikan HttpResponse yang berisi HTML inline error untuk HTMX.
    
    Args:
        error_msg (str): Pesan error yang akan ditampilkan.
        
    Returns:
        HttpResponse: Respons berisi HTML pesan error dan script update UI.
    """
    html = f"""
    <div id="urlInlineError" hx-swap-oob="true" class="error-message-inline">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        {error_msg}
    </div>

    <script>
        var input = document.getElementById('urlInput');
        input.classList.add('input-error');
        input.focus();
    </script>
    """
    return HttpResponse(html)

def process_analysis(request):
    """
    Logika umum untuk memproses permintaan analisis (ekstrak parameter, analisis, cache).
    Digunakan oleh view `index` dan `get_dataset` untuk menghindari duplikasi kode.
    
    Args:
        request: Objek HTTP request Django.
        
    Returns:
        tuple: (sukses, data_konteks_atau_error)
            - sukses (bool): True jika analisis berhasil, False jika gagal.
            - data_konteks_atau_error (dict): Data hasil analisis atau informasi error.
    """
    url, selected_limit, limit, video_count, comments_per_video = extract_analysis_params(request)
    

    user_channel_id = None
    yt_creds = request.session.get("yt_creds")
    if yt_creds and yt_creds.get("user"):
        user_channel_id = yt_creds.get("user").get("channel_id")

    analysis_result = analyze_content(url, limit, video_count, comments_per_video, user_channel_id=user_channel_id)
    
    error_msg = analysis_result["error_msg"]

    if error_msg:
        return False, {
            "error_message": error_msg,
            "url": url,
            "selected_limit": selected_limit
        }
    
    analysis_id = str(uuid.uuid4())
    cache_data = {
        "url": url,
        "limit": limit,
        "stats": analysis_result["stats"]
    }
    
    cache.set(f"analysis_data_{analysis_id}", cache_data, 600)
    
    return True, {
        "analysis_id": analysis_id,
        "url": url,
        "rows": analysis_result["results"],
        "selected_limit": selected_limit,
        "total_comments": analysis_result["stats"].get("total", 0),
        "judi_count": analysis_result["stats"].get("judi_count", 0),
        "clean_count": analysis_result["stats"].get("clean_count", 0),
        "source_info": analysis_result["source_info"],
    }

def refresh_user_session(request):
    """
    Memperbarui informasi pengguna di sesi jika kredensial ada dan valid.
    
    Args:
        request: Objek HTTP request Django.
        
    Returns:
        dict | None: Informasi pengguna terbaru atau None jika tidak ada kredensial.
    """
    yt_creds = request.session.get("yt_creds")
    if not yt_creds:
        return None

    try:
        creds_obj = Credentials(
            token=yt_creds["token"],
            refresh_token=yt_creds.get("refresh_token"),
            token_uri=yt_creds["token_uri"],
            client_id=yt_creds["client_id"],
            client_secret=yt_creds["client_secret"],
            scopes=yt_creds["scopes"],
        )
        fresh_user_info = fetch_youtube_user_info_oauth(creds_obj)
        
        yt_creds["user"] = fresh_user_info
        request.session["yt_creds"] = yt_creds
        return fresh_user_info
    except Exception as e:
        if settings.DEBUG:
            print(f"Failed to refresh user info: {e}")
        return yt_creds.get("user")

def map_moderation_error(error, debug_mode=False):
    """
    Memetakan HttpError dari YouTube API ke pesan yang mudah dipahami pengguna dan tipe error.
    
    Args:
        error (HttpError): Objek error dari library googleapiclient.
        debug_mode (bool): Jika True, detail error teknis akan disertakan.
        
    Returns:
        tuple: (pesan_msg, tipe_error, detail_teknis)
    """
    error_details = error.error_details[0] if error.error_details else {}
    reason = error_details.get('reason', 'unknown')
    
    if reason == 'processingFailure':
        msg = "Anda tidak memiliki izin untuk moderasi komentar di video ini. Pastikan Anda adalah pemilik channel/video."
        error_type = "no_permission"
    elif reason == 'forbidden':
        msg = "Akses ditolak. Anda tidak memiliki izin untuk melakukan moderasi."
        error_type = "forbidden"
    elif reason == 'commentNotFound':
        msg = "Komentar tidak ditemukan atau sudah dihapus."
        error_type = "not_found"
    else:
        msg = f"Gagal moderasi komentar: {error_details.get('message', str(error))}"
        error_type = "api_error"
        
    details = str(error) if debug_mode else None
    return msg, error_type, details
