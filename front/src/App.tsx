import './App.css';
import * as React from "react";
import MainTable from "./Components";
import './Components';


/*function getAnswersId() {
    let token = 'vk1.a.pykfcgaUdeb0JxdF5yOOIoqvGwCVYRUeHNPWxiM49T8kx8HGB5nB5huP97Ratm3sORpvlor24tg40-9j0CfY8xTX1n2bl1aZgor9bDKAroGyiXZidIRFJ4UX3dPS6GZarWt0OhMAlUDknV5jMLgLMzgvCey_9WJ3uoSn-fPwfWXc1UI02rSYylRHpEQT7Prro5B6aGguFQk7V4KxKwfumw'
    // console.log(token)
    let params = 'owner_id=736068632&is_board=0&poll_id=837100981&name_case=nom&v=5.131&access_token=' + token
    let req_url = 'https://api.vk.com/method/polls.getById?' + params;

    console.log(req_url);

    $.post({
        url: req_url,
        headers: {
            "accept": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        success: function (data) {
            console.log(data)
        }
    })
}*/


function App() {
    return (
        <div className="App">
            <MainTable/>
        </div>
    );
}


export default App;
