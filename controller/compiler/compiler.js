"use strict";

let config = require('../../config');

let {PythonShell} = require('python-shell');

let options = {
    mode: 'text',
    pythonPath: config.pythonPath,
    pythonOptions: ['-u'], // get print results in real-time
    scriptPath: config.acadelaBackEndPath
    // args: ['value1', 'value2', 'value3']
};

const compile = async (req, res) => {

    // const pythonProcess = await spawn('python', ["compiler.py"]);
    options.args = [req.body.code]
    // console.log('req body %j', req.body.code);
    const result1 = await PythonShell.run('compiler.py', options, function (err, results) {
        if (err) {
            console.log("Error");
            console.log(err);
            return res.status(213).json(err);
        }
        // Only return the result after the python script finishes executing
        else if (results) {
            // results is an array consisting of messages collected during execution
            console.log(`results: ${results.join("\n")}`);
            return res.status(201).json(`results: ${results.join("\n")}`);
        }
    });
     return result1;
}

module.exports = {
    compile
};
