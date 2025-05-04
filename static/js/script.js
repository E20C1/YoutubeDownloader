document.addEventListener('DOMContentLoaded', () => {
    // 要素の取得
    const youtubeUrlInput = document.getElementById('youtube-url');
    const searchBtn = document.getElementById('search-btn');
    const loadingElement = document.getElementById('loading');
    const errorMessageElement = document.getElementById('error-message');
    const videoInfoElement = document.getElementById('video-info');
    const videoThumbnail = document.getElementById('video-thumbnail');
    const videoTitle = document.getElementById('video-title');
    const videoAuthor = document.getElementById('video-author');
    const streamsContainer = document.getElementById('streams-container');
    const downloadStatusElement = document.getElementById('download-status');
    const progressBarInner = document.getElementById('progress-bar-inner');
    const downloadMessage = document.getElementById('download-message');
    const tabs = document.querySelectorAll('.tab');
    
    // 現在のURLを保存
    let currentUrl = '';
    let currentStreams = [];
    
    // エンターキーで検索ボタンを押す
    youtubeUrlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchBtn.click();
        }
    });
    
    // 検索ボタンのクリックイベント
    searchBtn.addEventListener('click', () => {
        const url = youtubeUrlInput.value.trim();
        
        if (!url) {
            showError('YouTube動画のURLを入力してね😊');
            return;
        }
        
        // URLをチェック（簡易的なチェック）
        if (!url.includes('youtube.com/watch') && !url.includes('youtu.be/')) {
            showError('YouTubeのURLじゃないみたい💦');
            return;
        }
        
        currentUrl = url;
        fetchVideoInfo(url);
    });
    
    // 動画情報を取得する関数
    async function fetchVideoInfo(url) {
        // UIをリセット
        resetUI();
        
        // ローディング表示
        loadingElement.classList.remove('hidden');
        
        try {
            const response = await fetch('/get_video_info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'エラーが発生しました');
            }
            
            // 動画情報を表示
            displayVideoInfo(data);
            
        } catch (error) {
            showError(error.message);
        } finally {
            // ローディング非表示
            loadingElement.classList.add('hidden');
        }
    }
    
    // 動画情報を表示する関数
    function displayVideoInfo(data) {
        currentStreams = data.streams;
        
        // サムネイル設定
        videoThumbnail.src = data.thumbnail_url;
        
        // タイトルと作者を設定
        videoTitle.textContent = data.title;
        videoAuthor.textContent = `作者: ${data.author}`;
        
        // ストリームのリストを表示
        renderStreams('all');
        
        // 動画情報を表示
        videoInfoElement.classList.remove('hidden');
    }
    
    // ストリームをレンダリングする関数
    function renderStreams(filterType) {
        streamsContainer.innerHTML = '';
        
        let filteredStreams = currentStreams;
        
        // フィルタリング
        if (filterType !== 'all') {
            filteredStreams = currentStreams.filter(stream => stream.type === filterType);
        }
        
        // ストリームがない場合
        if (filteredStreams.length === 0) {
            streamsContainer.innerHTML = '<p class="no-streams">利用可能なオプションがありません</p>';
            return;
        }
        
        // ストリームのリストを作成
        filteredStreams.forEach(stream => {
            const streamItem = document.createElement('div');
            streamItem.className = 'stream-item';
            
            let title, meta;
            
            // サーバーから送られてきたアイコンを使用するか、ない場合はデフォルトを設定
            const icon = stream.icon || (stream.mime_type.startsWith('audio') ? '🎵' : '🎥');
            
            if (stream.mime_type.startsWith('audio')) {
                title = `${icon} ${stream.resolution}`;
                meta = `形式: ${stream.mime_type} | タイプ: ${stream.type} | サイズ: ${stream.filesize} | 拡張子: ${stream.ext || 'm4a'}`;
            } else {
                title = `${icon} ${stream.resolution}`;
                meta = `形式: ${stream.mime_type} | タイプ: ${stream.type} | サイズ: ${stream.filesize} | 拡張子: ${stream.ext || 'mp4'}`;
            }
            
            streamItem.innerHTML = `
                <div class="stream-info">
                    <div class="stream-title">${title}</div>
                    <div class="stream-meta">${meta}</div>
                </div>
                <button class="download-btn" data-itag="${stream.format_id}">ダウンロード</button>
            `;
            
            streamsContainer.appendChild(streamItem);
        });
        
        // ダウンロードボタンにイベントリスナーを追加
        document.querySelectorAll('.download-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const itag = this.getAttribute('data-itag');
                downloadVideo(currentUrl, itag);
            });
        });
    }
    
    // 動画をダウンロードする関数
    async function downloadVideo(url, itag) {
        // ダウンロードステータスを表示
        downloadStatusElement.classList.remove('hidden');
        progressBarInner.style.width = '10%';
        downloadMessage.textContent = 'ダウンロードの準備中...';
        
        try {
            const response = await fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url, itag })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'ダウンロード中にエラーが発生しました');
            }
            
            // ダウンロード進行状況を更新
            progressBarInner.style.width = '100%';
            downloadMessage.textContent = 'ダウンロード完了！';
            
            // ダウンロードリンクを作成して自動クリック
            const downloadLink = document.createElement('a');
            downloadLink.href = data.download_path;
            downloadLink.style.display = 'none';
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
            
            // 少し待ってからステータスを非表示に
            setTimeout(() => {
                downloadStatusElement.classList.add('hidden');
            }, 3000);
            
        } catch (error) {
            progressBarInner.style.width = '0%';
            downloadMessage.textContent = `エラー: ${error.message}`;
            
            // 少し待ってからステータスを非表示に
            setTimeout(() => {
                downloadStatusElement.classList.add('hidden');
            }, 3000);
        }
    }
    
    // タブのクリックイベント
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // アクティブなタブをリセット
            tabs.forEach(t => t.classList.remove('active'));
            
            // クリックされたタブをアクティブに
            this.classList.add('active');
            
            // 選択されたタイプのストリームを表示
            const type = this.getAttribute('data-type');
            renderStreams(type);
        });
    });
    
    // エラーを表示する関数
    function showError(message) {
        errorMessageElement.textContent = message;
        errorMessageElement.classList.remove('hidden');
        videoInfoElement.classList.add('hidden');
    }
    
    // UIをリセットする関数
    function resetUI() {
        errorMessageElement.classList.add('hidden');
        videoInfoElement.classList.add('hidden');
        downloadStatusElement.classList.add('hidden');
    }
});
