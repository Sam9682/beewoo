// Generated automatically by nearley
// http://github.com/Hardmath123/nearley
(function () {
function id(x) {return x[0]; }

var appendItem = function(a, b, c) { return function(z) { return z[a].concat(":").concat(z[b]).concat(":").concat(z[c]); } };
var appendIPItem = function(a, b, c, d) { return function(z) { return z[a].concat(".").concat(z[b]).concat(".").concat(z[c]).concat(".").concat(z[d]); } };
var appendItemChar = function(a, b) { return function(z) { return z[a].concat(z[b]); } };
var empty = function() {};
var emptyStr = function(d) { return ""; };
var grammar = {
    Lexer: undefined,
    ParserRules: [
    {"name": "row", "symbols": ["time", "_", "prot", "_", "addr_from", "_", {"literal":">"}, "_", "addr_to", {"literal":":"}, "_", "opts", "newline"], "postprocess": function(d) { return { time: d[0], prot: d[2], addr_from: d[4], addr_to: d[8], opts: d[10] }; }},
    {"name": "time", "symbols": ["integer", {"literal":":"}, "integer", {"literal":":"}, "integer", {"literal":"."}, "integer"], "postprocess": appendItem(0,2,4)},
    {"name": "prot", "symbols": ["alphas"], "postprocess": function(z) { return z[0]; }},
    {"name": "length", "symbols": ["integer"], "postprocess": id},
    {"name": "addr_from", "symbols": ["integer", {"literal":"."}, "integer", {"literal":"."}, "integer", {"literal":"."}, "integer", {"literal":"."}, "integer"], "postprocess": appendIPItem(0,2,4,6)},
    {"name": "addr_from", "symbols": ["integer", {"literal":"."}, "integer", {"literal":"."}, "integer", {"literal":"."}, "integer", {"literal":"."}, "alphas"], "postprocess": appendIPItem(0,2,4,6)},
    {"name": "addr_from", "symbols": ["alphanums", {"literal":"."}, "alphanums", {"literal":"."}, "alphanums", {"literal":"."}, "integer"], "postprocess": appendIPItem(0,2,4,6)},
    {"name": "addr_from", "symbols": ["alphanums", {"literal":"."}, "alphanums", {"literal":"."}, "alphanums", {"literal":"."}, "alphas"], "postprocess": appendIPItem(0,2,4,6)},
    {"name": "addr_from", "symbols": ["alphanums", {"literal":"."}, "integer"], "postprocess": function(z) { return z[0]; }},
    {"name": "addr_from", "symbols": ["alphanums", {"literal":"."}, "alphas"], "postprocess": function(z) { return z[0]; }},
    {"name": "addr_to", "symbols": ["integer", {"literal":"."}, "integer", {"literal":"."}, "integer", {"literal":"."}, "integer", {"literal":"."}, "integer"], "postprocess": appendIPItem(0,2,4,6)},
    {"name": "addr_to", "symbols": ["integer", {"literal":"."}, "integer", {"literal":"."}, "integer", {"literal":"."}, "integer", {"literal":"."}, "alphas"], "postprocess": appendIPItem(0,2,4,6)},
    {"name": "addr_to", "symbols": ["alphanums", {"literal":"."}, "alphanums", {"literal":"."}, "alphanums", {"literal":"."}, "integer"], "postprocess": appendIPItem(0,2,4,6)},
    {"name": "addr_to", "symbols": ["alphanums", {"literal":"."}, "alphanums", {"literal":"."}, "alphanums", {"literal":"."}, "alphas"], "postprocess": appendIPItem(0,2,4,6)},
    {"name": "addr_to", "symbols": ["alphanums", {"literal":"."}, "integer"], "postprocess": function(z) { return z[0]; }},
    {"name": "addr_to", "symbols": ["alphanums", {"literal":"."}, "alphas"], "postprocess": function(z) { return z[0]; }},
    {"name": "opts$ebnf$1", "symbols": [/[^\\]/]},
    {"name": "opts$ebnf$1", "symbols": ["opts$ebnf$1", /[^\\]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "opts", "symbols": ["opts$ebnf$1"], "postprocess": function(z) { return z[0]; }},
    {"name": "port", "symbols": ["integer"]},
    {"name": "port", "symbols": ["alphas"], "postprocess": function(z) { return z[0]; }},
    {"name": "integer$ebnf$1", "symbols": [/[0-9]/]},
    {"name": "integer$ebnf$1", "symbols": ["integer$ebnf$1", /[0-9]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "integer", "symbols": ["integer$ebnf$1"], "postprocess": function(z) { return z[0]; }},
    {"name": "alphas$ebnf$1", "symbols": [/[a-zA-Z]/]},
    {"name": "alphas$ebnf$1", "symbols": ["alphas$ebnf$1", /[a-zA-Z]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "alphas", "symbols": ["alphas$ebnf$1"], "postprocess": function(z) { return z[0]; }},
    {"name": "alphanums$ebnf$1", "symbols": [/[a-zA-Z0-9\-\_]/]},
    {"name": "alphanums$ebnf$1", "symbols": ["alphanums$ebnf$1", /[a-zA-Z0-9\-\_]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "alphanums", "symbols": ["alphanums$ebnf$1"], "postprocess": function(z) { return z[0]; }},
    {"name": "newline", "symbols": []},
    {"name": "newline", "symbols": [{"literal":"\r"}, {"literal":"\n"}]},
    {"name": "newline", "symbols": [{"literal":"\n"}, {"literal":"\r"}], "postprocess": empty},
    {"name": "_", "symbols": []},
    {"name": "_", "symbols": ["_", /[ \t]/], "postprocess": empty}
]
  , ParserStart: "row"
}
if (typeof module !== 'undefined'&& typeof module.exports !== 'undefined') {
   module.exports = grammar;
} else {
   window.grammar = grammar;
}
})();
