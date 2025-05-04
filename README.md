# 🎥 YouTube ダウンローダー

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Framework: Flask](https://img.shields.io/badge/Framework-Flask-orange.svg)](https://flask.palletsprojects.com/)

<p align="center">
  <img src="assets/icons/icon128.png" alt="YouTube Downloader" width="128">
</p>

> 教育目的で作られた軽量WebベースのYouTubeダウンロードツールです。

## 📝 目次

- [機能概要](#機能概要-)
- [セットアップ方法](#セットアップ方法-)
- [使い方](#使い方-)
- [動作の仕組み](#動作の仕組み-)
- [注意事項](#注意事項-)
- [トラブルシューティング](#トラブルシューティング-)

## 機能概要 ✨

<table align="center">
  <tr>
    <td align="center">📹<br><b>高品質動画</b></td>
    <td align="center">🎧<br><b>音声ダウンロード</b></td>
    <td align="center">💾<br><b>簡単操作</b></td>
  </tr>
  <tr>
    <td align="center">🔍<br><b>動画情報表示</b></td>
    <td align="center">💻<br><b>ローカルホスト実行</b></td>
    <td align="center">🚀<br><b>軽量設計</b></td>
  </tr>
</table>

- **複数の品質オプション**: 4K、1080p、720p、360pの解像度から選択可能
- **高品質音声ダウンロード**: m4a形式で音声のみをダウンロード可能
- **動画メタデータ表示**: タイトル、サムネイル、サイズ情報を表示
- **シンプルなUI**: 初心者でも使いやすい直感的なインターフェース

## セットアップ方法 💻

### 必要なソフトウェア

<table>
  <tr>
    <td align="center" width="120">🔥</td>
    <td><b>Python 3.7以上</b><br>Pythonがインストールされていない場合は<a href="https://www.python.org/downloads/">Python公式サイト</a>からダウンロードしてください</td>
  </tr>
  <tr>
    <td align="center">🗜️</td>
    <td><b>ffmpeg (必須)</b><br>動画・音声の変換処理に必要なツールです。下記の「<a href="#ffmpegのインストール方法-">インストール方法</a>」を参照してインストールしてください</td>
  </tr>
</table>

### セットアップ手順

<div align="center">

| ステップ | 操作 | 説明 |
|:---:|:---|:---|
| 1📦 | **ファイルをダウンロード** | GitHubからZIPファイルをダウンロードして解凍します |
| 2📐 | **プロジェクトフォルダを開く** | コマンドプロンプトでフォルダに移動します |
| 3📯 | **依存関係をインストール** | `pip install -r requirements.txt` を実行します |
| 4🌟 | **アプリを起動** | `start_app.bat` をダブルクリックします |

</div>

```bash
# コマンドラインからセットアップする場合
# 1. プロジェクトフォルダに移動
> cd フォルダのパス

# 2. 依存関係をインストール
> pip install -r requirements.txt
```

## 使い方 👁‍🗨

### 基本的な使い方

<div align="center">
  <table>
    <tr>
      <td align="center" width="60">🔃</td>
      <td><b>アプリを起動</b></td>
      <td>フォルダ内の <code>start_app.bat</code> をダブルクリック</td>
    </tr>
    <tr>
      <td align="center">🌐</td>
      <td><b>ブラウザが開く</b></td>
      <td>自動的に <a href="http://localhost:5000">http://localhost:5000</a> にアクセスされます</td>
    </tr>
    <tr>
      <td align="center">🔎</td>
      <td><b>URLを入力</b></td>
      <td>YouTube動画のURLを入力して「検索」ボタンをクリック</td>
    </tr>
    <tr>
      <td align="center">📹</td>
      <td><b>解像度を選択</b></td>
      <td>表示された品質オプションから希望のものを選択</td>
    </tr>
    <tr>
      <td align="center">⬇️</td>
      <td><b>ダウンロード</b></td>
      <td>「ダウンロード」ボタンをクリックしてファイルを保存</td>
    </tr>
  </table>
</div>

### 手動で起動する場合

`start_app.bat` ファイルが使えない場合は、以下の手順で起動できます：

```bash
# アプリケーションを起動
> py app.py

# ブラウザで以下のURLにアクセス
# http://localhost:5000
```

## 動作の仕組み 🔧

<div align="center">
  <code>URL入力</code> ➡️ <code>サーバーに送信</code> ➡️ <code>yt-dlpで動画情報取得</code> ➡️ <code>メタデータ・サムネイル表示</code> ➡️ <code>品質選択</code> ➡️ <code>ダウンロード実行</code> ➡️ <code>ffmpegで処理</code> ➡️ <code>ファイル保存</code>
</div>

<div align="center">
  <table>
    <tr>
      <td align="center"><b>💻 フロントエンド</b></td>
      <td align="center">↔️</td>
      <td align="center"><b>🖥️ Flaskサーバー</b></td>
      <td align="center">↔️</td>
      <td align="center"><b>🎥 YouTube API</b></td>
    </tr>
  </table>
</div>

### 使用している技術

<table align="center">
  <tr>
    <td align="center" width="100">🌐</td>
    <td><b>Flask</b></td>
    <td>Python製の軽量ウェブフレームワークで、サーバーとブラウザ間の通信を管理します</td>
  </tr>
  <tr>
    <td align="center">📼</td>
    <td><b>yt-dlp</b></td>
    <td>YouTubeの動画情報やメタデータを取得し、ファイルのダウンロードを行うライブラリです</td>
  </tr>
  <tr>
    <td align="center">🎥</td>
    <td><b>FFmpeg</b></td>
    <td>動画のフォーマット変換や音声・動画の結合を行うツールです</td>
  </tr>
  <tr>
    <td align="center">📦</td>
    <td><b>JavaScript</b></td>
    <td>ブラウザ上でのインターフェースとユーザー操作を実現します</td>
  </tr>
</table>

### ファイル構成

```
YoutubeDownloader/
├─ app.py         # Flaskアプリのメインファイル
├─ start_app.bat   # アプリケーション起動用バッチファイル
├─ static/        # 静的ファイルディレクトリ
│   ├─ css/        # CSSスタイルシート
│   │   └─ style.css
│   └─ js/         # JavaScriptファイル
│       └─ script.js
├─ templates/     # HTMLテンプレート
│   └─ index.html
├─ downloads/     # ダウンロードされたファイルの一時保存場所
├─ requirements.txt  # 必要なパッケージリスト
└─ README.md      # このファイル
```

## 注意事項 ⚠️

<div align="center">
  <table>
    <tr>
      <td align="center" width="60">🎓</td>
      <td><b>教育目的限定</b></td>
      <td>このツールは学習や教育目的での利用を想定しています</td>
    </tr>
    <tr>
      <td align="center">©️</td>
      <td><b>著作権尊重</b></td>
      <td>著作権で保護されたコンテンツは適切な権利を持つ場合のみダウンロードしてください</td>
    </tr>
    <tr>
      <td align="center">📜</td>
      <td><b>利用規約</b></td>
      <td>YouTubeの利用規約では、動画のダウンロードが制限されている場合があります</td>
    </tr>
    <tr>
      <td align="center">🚫</td>
      <td><b>商用利用禁止</b></td>
      <td>このツールを商用目的や違法な目的で使用しないでください</td>
    </tr>
  </table>
</div>

## トラブルシューティング 🔧

<div align="center">

| 問題 | 原因 | 解決方法 |
|:---|:---|:---|
| **アプリが起動しない** | Pythonが見つからないかライブラリの問題 | ・`pip install -r requirements.txt`を実行してください<br>・Pythonがインストールされているか確認してください |
| **動画情報取得エラー** | URLの形式が間違っている可能性 | ・YouTubeのURLが正しい形式か確認してください<br>・別の動画で試してみてください |
| **ダウンロードが失敗する** | ネットワーク問題まFFmpegの問題 | ・インターネット接続を確認してください<br>・FFmpegが正しくインストールされているか確認してください |
| **m4aファイルが開けない** | 音声ファイル変換の失敗 | ・他の動画の音声ダウンロードを試してください<br>・動画ダウンロードを代わりに試してください |

</div>

### よくある質問

<details>
<summary><b>Q: Windows以外の環境でも使えますか？</b></summary>

A: はい、PythonとFFmpegがインストールされていれば、MacやLinuxでも動作します。ただし、`start_app.bat`は使用できないため、純粋なPythonコマンドで起動してください。
</details>

<details>
<summary><b>Q: ダウンロードしたファイルはどこに保存されますか？</b></summary>

A: ダウンロードしたファイルは一時的に`downloads`フォルダに保存され、ブラウザ経由であなたのダウンロードフォルダに保存されます。
</details>

## 開発者向け情報 💻

### 機能拡張ガイド

このアプリケーションは拡張しやすい設計になっています。以下は主な機能拡張ポイントです：

<table>
  <tr>
    <td align="center" width="80">📡</td>
    <td><b>ダウンロード形式の追加</b></td>
    <td><code>app.py</code> の <code>get_video_info()</code> 関数を編集して形式を追加します</td>
  </tr>
  <tr>
    <td align="center">💾</td>
    <td><b>保存先カスタマイズ</b></td>
    <td><code>app.py</code> の先頭にある <code>DOWNLOAD_FOLDER</code> 変数を編集します</td>
  </tr>
  <tr>
    <td align="center">🎨</td>
    <td><b>UIデザイン変更</b></td>
    <td><code>static/css/style.css</code> と <code>templates/index.html</code> を編集します</td>
  </tr>
</table>

### 依存ライブラリ

このアプリケーションは以下の主要ライブラリに依存しています：

```
Flask==2.0.1
Werkzeug==2.0.3
yt-dlp>=2023.3.4
```

### ローカル開発環境のセットアップ

開発を始めるには以下の手順で仮想環境を作成することをお勧めします：

```bash
# 仮想環境を作成
> python -m venv venv

# 仮想環境を有効化（Windows）
> venv\Scripts\activate

# 仮想環境を有効化（Mac/Linux）
$ source venv/bin/activate

# 依存関係のインストール
> pip install -r requirements.txt
```

## ffmpegのインストール方法 📹

アプリケーションを使用するには、ffmpegが必要です。以下の手順でインストールしてください。

### Windowsでのインストール方法

1. **公式サイトからダウンロード**
   - [FFmpeg公式ダウンロードページ](https://ffmpeg.org/download.html) にアクセス
   - 「Windows」セクションから「Windows builds from gyan.dev」を選択
   - [ダウンロードページ(gyan.dev)](https://www.gyan.dev/ffmpeg/builds/) から「ffmpeg-release-essentials.zip」をダウンロード

2. **ファイルを解凍**
   - ダウンロードしたZIPファイルを解凍
   - 解凍したフォルダの中にある`bin`フォルダを開く
   - `ffmpeg.exe`ファイルを見つける

3. **プロジェクトに配置**
   - `ffmpeg.exe`をこのプロジェクトのルートディレクトリ（app.pyと同じ場所）にコピー

### macOSでのインストール方法

1. **Homebrewを使用してインストール**
   ```bash
   brew install ffmpeg
   ```

2. **パスを確認**
   ```bash
   which ffmpeg
   ```
   上記コマンドで表示されるパスをメモしておく

3. **プロジェクトの設定を変更**
   - `app.py`を開き、先頭部分にある`FFMPEG_PATH`変数があれば、それを先ほど確認したパスに設定

### Linuxでのインストール方法

1. **パッケージマネージャーでインストール**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install ffmpeg
   
   # Fedora
   sudo dnf install ffmpeg
   ```

2. **パスを確認**
   ```bash
   which ffmpeg
   ```

### 注意事項

- ffmpegが正しくインストールされていない場合、動画のダウンロード時に次のようなエラーが表示されることがあります：
  ```
  ERROR: ffmpeg not found. Please install ffmpeg.
  ```

- Windowsでは、PATHを通してffmpegをシステム全体で使えるようにする方法もありますが、初心者の方は上記のようにプロジェクトフォルダに直接配置する方法が簡単です。

## ライセンス 📃

MIT License

Copyright (c) 2025 YouTubeDownloader

This software is provided for educational purposes only. Personal use is permitted.

---

<div align="center">作成者: E20C1</div>
<div align="center">最終更新日: 2025年5月4日</div>
