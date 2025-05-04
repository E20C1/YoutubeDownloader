from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import uuid
import re
import time
import logging
import json

# ログ設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# 一時的なダウンロードフォルダ
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# yt-dlpのオプション
YDL_OPTS = {
    'quiet': True, 
    'no_warnings': True,
    'skip_download': True,
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'noplaylist': True,
    'merge_output_format': 'mp4',
}

# 古いファイルを削除（24時間以上経過したもの）
def cleanup_downloads():
    current_time = time.time()
    for filename in os.listdir(DOWNLOAD_FOLDER):
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        # ファイルの経過時間を確認
        if os.path.isfile(file_path) and (current_time - os.path.getmtime(file_path)) > 86400:
            os.remove(file_path)

# 動画形式を整理する関数
def format_filesize(bytes):
    """Convert bytes to human-readable format"""
    if bytes is None:
        return "Unknown"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024 or unit == 'GB':
            return f"{bytes:.1f} {unit}"
        bytes /= 1024

@app.route('/')
def index():
    cleanup_downloads()
    return render_template('index.html')

@app.route('/get_video_info', methods=['POST'])
def get_video_info():
    data = request.get_json()
    url = data.get('url', '')
    
    logging.debug(f"受け取ったURL: {url}")
    
    if not url:
        return jsonify({'error': 'URLが入力されていません。'}), 400
    
    # YouTube URLの検証
    youtube_regex = r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/)([^"&?/ ]{11})'
    youtube_match = re.search(youtube_regex, url)
    
    if not youtube_match and ('youtube.com/' not in url and 'youtu.be/' not in url):
        logging.debug(f"URLが一致しません: {url}")
        return jsonify({'error': 'YouTubeのURLを入力して下さい。'}), 400
    
    try:
        # もっとシンプルな実装に変更
        logging.debug("動画情報取得開始")
        
        # yt-dlpを使って動画情報を取得
        with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(url, download=False)
            
        # 実際の音声ビットレートとファイルサイズを取得
        audio_bitrate = None
        audio_filesize = 0
        video_4k_filesize = 0    # 4Kサイズを追加
        video_1440p_filesize = 0  # 1440pサイズを追加
        video_1080p_filesize = 0
        video_720p_filesize = 0
        video_360p_filesize = 0
        
        # 利用可能な解像度をチェック
        has_4k = False
        has_1440p = False
        has_1080p = False
        has_720p = False
        has_360p = False
        
        # 全形式をチェックしてビットレートとサイズを取得
        for f in info.get('formats', []):
            # 音声データのビットレート取得
            if f.get('acodec') != 'none' and f.get('abr') and f.get('ext') == 'm4a':
                # 音声データのビットレートとサイズを保存
                if audio_bitrate is None or f.get('abr') > audio_bitrate:
                    audio_bitrate = f.get('abr')
                    if f.get('filesize'):
                        audio_filesize = f.get('filesize')
            
            # 動画のサイズを取得と利用可能な解像度をチェック
            if f.get('vcodec') != 'none' and f.get('height'):
                # 4K動画サイズ取得 (2160p)
                if f.get('height') >= 2160:
                    has_4k = True
                    if f.get('filesize') and (video_4k_filesize == 0 or f.get('filesize') > video_4k_filesize):
                        video_4k_filesize = f.get('filesize')
                # 1440p動画サイズ取得
                elif f.get('height') >= 1440 and f.get('height') < 2160:
                    has_1440p = True
                    if f.get('filesize') and (video_1440p_filesize == 0 or f.get('filesize') > video_1440p_filesize):
                        video_1440p_filesize = f.get('filesize')
                # 1080p動画サイズ取得
                elif f.get('height') >= 1080 and f.get('height') < 1440:
                    has_1080p = True
                    if f.get('filesize') and (video_1080p_filesize == 0 or f.get('filesize') > video_1080p_filesize):
                        video_1080p_filesize = f.get('filesize')
                # 720p動画サイズ取得
                elif f.get('height') >= 720 and f.get('height') < 1080:
                    has_720p = True
                    if f.get('filesize') and (video_720p_filesize == 0 or f.get('filesize') > video_720p_filesize):
                        video_720p_filesize = f.get('filesize')
                # 360p動画サイズ取得
                elif f.get('height') <= 480:
                    has_360p = True
                    if f.get('filesize') and (video_360p_filesize == 0 or f.get('filesize') > video_360p_filesize):
                        video_360p_filesize = f.get('filesize')
        
        # サイズが取得できなかった場合は予測値を設定
        if audio_filesize == 0:
            audio_filesize = 3 * 1024 * 1024  # 約3MB
        if video_4k_filesize == 0:
            video_4k_filesize = 40 * 1024 * 1024  # 約40MB
        if video_1440p_filesize == 0:
            video_1440p_filesize = 25 * 1024 * 1024  # 約25MB
        if video_1080p_filesize == 0:
            video_1080p_filesize = 15 * 1024 * 1024  # 約15MB
        if video_720p_filesize == 0:
            video_720p_filesize = 8 * 1024 * 1024  # 約8MB
        if video_360p_filesize == 0:
            video_360p_filesize = 3 * 1024 * 1024  # 約3MB
            
        # ファイルサイズをメガバイト表示に変換する関数
        def format_filesize(size_bytes):
            if size_bytes <= 0:
                return "?　MB"
            size_mb = size_bytes / (1024 * 1024)
            return f"{size_mb:.2f} MB"
        
        # 利用可能な形式を取得
        formats = []
        
        # 実際に利用可能なビデオ解像度のみ追加
        
        # 4K動画用の形式
        if has_4k:
            uhd_video = {
                'format_id': 'bestvideo[height>=2160][ext=mp4]+bestaudio[ext=m4a]/best[height>=2160]/best',
                'resolution': '4K (2160p)',
                'ext': 'mp4',
                'filesize': format_filesize(video_4k_filesize + audio_filesize),
                'type': '超高品質動画',
                'mime_type': 'video/mp4',
                'icon': '🎥'  # ビデオカメラアイコン
            }
            formats.append(uhd_video)
        
        # 1440p動画用の形式
        if has_1440p:
            qhd_video = {
                'format_id': 'bestvideo[height>=1440][height<2160][ext=mp4]+bestaudio[ext=m4a]/best[height>=1440][height<2160]/best',
                'resolution': '1440p',
                'ext': 'mp4',
                'filesize': format_filesize(video_1440p_filesize + audio_filesize),
                'type': '高品質動画',
                'mime_type': 'video/mp4',
                'icon': '🎥'  # ビデオカメラアイコン
            }
            formats.append(qhd_video)
        
        # 1080p動画用の形式
        if has_1080p:
            best_video = {
                'format_id': 'bestvideo[height>=1080][height<1440][ext=mp4]+bestaudio[ext=m4a]/best[height>=1080][height<1440]/best',
                'resolution': '1080p',
                'ext': 'mp4',
                'filesize': format_filesize(video_1080p_filesize + audio_filesize),
                'type': '高品質動画',
                'mime_type': 'video/mp4',
                'icon': '🎥'  # ビデオカメラアイコン
            }
            formats.append(best_video)
        
        # 標準動画用の形式
        if has_720p:
            standard_video = {
                'format_id': 'bestvideo[height>=720][height<1080][ext=mp4]+bestaudio[ext=m4a]/best[height>=720][height<1080]/best',
                'resolution': '720p',
                'ext': 'mp4',
                'filesize': format_filesize(video_720p_filesize + audio_filesize),
                'type': '映像+音声',
                'mime_type': 'video/mp4',
                'icon': '🎥'  # ビデオカメラアイコン
            }
            formats.append(standard_video)
        
        # 低画質動画用の形式
        if has_360p:
            low_video = {
                'format_id': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]/worst[ext=mp4]/worst',
                'resolution': '360p',
                'ext': 'mp4',
                'filesize': format_filesize(video_360p_filesize + audio_filesize),
                'type': '映像+音声',
                'mime_type': 'video/mp4',
                'icon': '🎥'  # ビデオカメラアイコン
            }
            formats.append(low_video)
        
        # 音声のみの形式 - 最高品質を優先
        audio_only = {
            'format_id': 'bestaudio[ext=m4a]/bestaudio',  # m4a形式を優先的に取得する
            'resolution': f'{audio_bitrate}kbps' if audio_bitrate else '最高音質',  
            'ext': 'm4a',
            'filesize': format_filesize(audio_filesize),
            'type': '音声',  # 音声と表示
            'mime_type': 'audio/m4a',
            'icon': '🎵'  # 音符マークを追加
        }
        formats.append(audio_only)
        
        # サムネイルと動画情報を取得
        thumbnail = info.get('thumbnail')
        title = info.get('title', '無題')
        author = info.get('uploader', '不明')
        
        video_info = {
            'title': title,
            'author': author,
            'thumbnail_url': thumbnail if thumbnail else '',
            'streams': formats
        }
        
        logging.debug(f"動画情報取得成功: タイトル={title}")
        return jsonify(video_info)
    
    except Exception as e:
        logging.exception(f"動画情報取得中にエラー発生: {str(e)}")
        return jsonify({'error': f'ERROR 500 取得できませんでした。'}), 500

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url', '')
    format_id = data.get('itag')
    
    logging.debug(f"ダウンロードリクエスト: URL={url}, format_id={format_id}")
    
    if not url or not format_id:
        return jsonify({'error': '必要なパラメータが不足しています🙁'}), 400
    
    try:
        # タイトルを取得してファイル名に使う
        with yt_dlp.YoutubeDL({}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', '')
            
        # ファイル名に使えるようにタイトルを整形
        # 日本語などの非アスキー文字をアルファベットにローマ字化するためのSlug化
        def slugify(text):
            # Unicode文字をASCIIに変換し、非アスキー文字を除去または置換
            import unicodedata
            import re
            
            # Unicode文字を正規化してASCIIに変換
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
            # 必要ない文字を除去
            text = re.sub(r'[^\w\s-]', '', text.lower())
            # 空白とハイフンをアンダースコアに置換
            text = re.sub(r'[\s-]+', '_', text).strip('-_')
            
            # 空だったらデフォルト値に
            if not text:
                text = 'youtube_audio'
                
            return text
        
        # 通常のファイル名の無効な文字を除去
        safe_title = re.sub(r'[\\/*?:"<>|]', '_', title)  # 不正な文字を置換
        safe_title = safe_title[:50] if len(safe_title) > 50 else safe_title  # 長すぎるタイトルを切り詰め
        
        # 非英数字が含まれている場合は、英数字のみに変換する
        if any(ord(c) > 127 for c in safe_title):
            slug_title = slugify(safe_title)
            # 日本語などが完全に無視された場合はユニークIDで代用
            if not slug_title:
                slug_title = 'youtube_' + str(uuid.uuid4())[:8]
            safe_title = slug_title
        
        # 同じ名前のファイルがあれば上書きされるリスクがあるが、ユーザーの要望でIDを付けない
        file_path = os.path.join(DOWNLOAD_FOLDER, safe_title)
        
        # 音声のみか動画かを判定
        is_audio_only = 'bestaudio' in format_id and not 'bestvideo' in format_id
        
        # ダウンロードオプションの初期化
        download_opts = {
            'format': format_id,
            'outtmpl': f"{file_path}.%(ext)s",
            'quiet': False,  # ログを表示することでデバッグしやすくする
            'no_warnings': False,
            'noplaylist': True,
        }
        
        # 音声のみの場合と動画の場合で処理を分ける
        if is_audio_only:
            # 音声ファイル用の設定 - 超シンプル版
            # 直接m4aをダウンロードする方式に変更
            download_opts['format'] = 'bestaudio[ext=m4a]/bestaudio'
            download_opts['outtmpl'] = f"{file_path}.%(ext)s"
            
            # ポストプロセッサは一切使わない - 変換なしでオリジナルファイルのまま
            # FFmpegオプションを全て無効化
            download_opts['postprocessors'] = []
            
            # ヘッドレスモードにしてよりシンプルに
            download_opts['quiet'] = True
        else:
            download_opts['merge_output_format'] = 'mp4'
            download_opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]
        
        logging.debug("ダウンロード開始")
        
        # ダウンロード実行
        with yt_dlp.YoutubeDL(download_opts) as ydl:
            ydl.download([url])
        
        # ダウンロードされたファイルを探す
        downloaded_filename = None
        for f in os.listdir(DOWNLOAD_FOLDER):
            if f.startswith(safe_title):
                downloaded_filename = f
                break
        
        if not downloaded_filename:
            logging.error("ダウンロードファイルが見つかりません")
            return jsonify({'error': 'あらら、ダウンロードに失敗しちゃったみたい。別の形式で試してみて！😢'}), 500
        
        logging.debug(f"ダウンロード完了: {downloaded_filename}")
        
        # ファイルの拡張子でcontent typeを判断
        file_extension = os.path.splitext(downloaded_filename)[1].lower()
        
        if file_extension in ['.mp4', '.webm', '.mkv']:
            content_type = 'video/mp4'
        elif file_extension in ['.mp3', '.m4a', '.aac', '.wav']:
            content_type = 'audio/mp3'
        else:
            content_type = 'application/octet-stream'
        
        return jsonify({
            'success': True,
            'message': 'ダウンロード完了！🎉 楽しんでね～♪',
            'download_path': f'/get_file/{downloaded_filename}',
            'content_type': content_type
        })
    
    except Exception as e:
        logging.exception(f"ダウンロード中にエラー発生: {str(e)}")
        return jsonify({'error': f'あちゃー！ダウンロードできなかったよ😥 別の動画や形式で試してみて！'}), 500

@app.route('/get_file/<filename>')
def get_file(filename):
    return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
