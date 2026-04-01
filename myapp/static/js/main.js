document.addEventListener('DOMContentLoaded', function() {
    const fetchButton = document.getElementById('fetchDataButton');
    const dataDisplayArea = document.getElementById('dataDisplay');
    const datainput_Area = document.getElementById('input_area');
    const dataoutput_Area = document.getElementById('output_area');
    const select_data = document.getElementById('select');
    const footer_data = document.getElementById('footer');
    if (fetchButton && dataDisplayArea && datainput_Area && 
        dataoutput_Area && select_data) {
    
    //if (fetchButton && dataDisplayArea  && 
        //dataoutput_Area) {
        fetchButton.addEventListener('click', function() {
            dataDisplayArea.textContent = 'データ取得中...'; // ローディング表示

            fetch('/api/data') // FlaskのAPIエンドポイントを呼び出す
                .then(response => {
                    if (!response.ok) {
                        // okプロパティはステータスコードが200-299の範囲ならtrue
                        throw new Error('ネットワークレスポンスエラー Status: ' + response.status);
                    }
                    return response.json(); // JSONに変換するPromiseを返す
                })
                .then(data => {
                    // JSONデータの取得成功
                    console.log('サーバーから受信:', data);
                    const displayTime = new Date(data.timestamp).toLocaleString('ja-JP'); // 見やすい形式に
                    
                    dataDisplayArea.textContent = `取得値: ${data.value} (ステータス: ${data.status}, 取得時刻: ${displayTime})`;
                    //dataoutput_Area.value = select_data.value;
                    dataoutput_Area.value = datainput_Area.value;
                    footer_data.textContent = select_data.value;
                })
                .catch(error => {
                    // エラーハンドリング
                    console.error('Fetch処理中にエラーが発生しました:', error);
                    dataDisplayArea.textContent = 'データの取得に失敗しました。コンソールを確認してください。';
                });
        });
    } else {
        console.error('データ取得ボタンまたは表示エリアが見つかりません。IDを確認してください。');
    }
});