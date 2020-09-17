"use strict";

const compile = async (req, res) => {
    return res.status(201).json({"success":"cool"});
}

module.exports = {
    compile
};