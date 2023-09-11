
import axios from 'axios';

export default class HttpService {

    static header =
        {
            headers:
            {
                "Content-Type": "application/json",
                "simulateuser": "mustermann@test.sc"
            }
        }

    static async post(url, data, onSuccess, onError) {
        await axios.post(url, JSON.stringify(data), header)
            .then(function (data) {
                onSuccess(data);
            })
            .catch(function (error) {
                onError(error);
            });
    };

}