"use strict";

let {PythonShell} = require('python-shell')
let options = {
    mode: 'text',
    pythonPath: 'C:\\Program Files (x86)\\Microsoft Visual Studio\\Shared\\Python36_64\\python.exe',
    pythonOptions: ['-u'], // get print results in real-time
    scriptPath: 'E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\acadela'
    // args: ['value1', 'value2', 'value3']
};

const compile = async (req, res) => {
    // const pythonProcess = await spawn('python', ["compiler.py"]);
    options.args = [req.body.code]
    console.log('req body %j', req.body.code);
    await PythonShell.run('compiler.py', options, function (err, results) {
        if (err) {
            console.log("Error");
            console.log(err);
        }
        // results is an array consisting of messages collected during execution
        console.log('results: %s', results.join("\n"));
    });
    return res.status(201).json({"Success": "ok"});

}

module.exports = {
    compile
};