
import axios from 'axios';

export default class HttpService {

    static async post(url, data, onSuccess, onError) {
        await axios.post(url,
            JSON.stringify(data),
            { headers: { 'Content-Type': 'application/json' }})
            .then(function (data) {
                onSuccess(data);
            })
            .catch(function (error) {
                onError(error);
            });
    };
}