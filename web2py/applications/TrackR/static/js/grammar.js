// Generated automatically by nearley
// http://github.com/Hardmath123/nearley
(function () {
function id(x) {return x[0]; }


var readTime = function(z) {
	var chaine = '';
	chaine = z.join('');
	chaine = chaine.replace(/,/g,'');
	return(chaine);
};

var readProtocol = function(z) {
	var chaine = '';
	chaine = z.join('');
	chaine = chaine.replace(/,/g,'');
	return(chaine);
};

var readNameFrom = function(z) {
	var chaine1 = '', chaine2 = '';
	chaine1 = z[0].join('');
	chaine1 = chaine1.replace(/,/g,'');
	chaine1 = chaine1.slice(0,-1);
	chaine2 = z[1];
	chaine2 = chaine2.replace(/,/g,'');
	res = { addr_from: chaine1, port_from: chaine2 };
	return(res);
};

var readNameTo = function(z) {
	var chaine1 = '', chaine2 = '';
	chaine1 = z[0].join('');
	chaine1 = chaine1.replace(/,/g,'');
	chaine1 = chaine1.slice(0,-1);
	chaine2 = z[1];
	chaine2 = chaine2.replace(/,/g,'');
	res = { addr_to: chaine1, port_to: chaine2 };
	return(res);
};

var readMachName = function(a,b,c) { return function(z) { return { from: z[a] + z[b] + z[c] } } };

var readPort = function(z) {
	res = { MACHINE: z[0] };
	return(res);
};

var readBody = function(z) {
	var chaine = '';
	chaine = z.join('');
	chaine = chaine.replace(/,/g,'');
	return(chaine);
};

var empty = function() { return null };

var emptyStr = function(d) { return ""; };
var grammar = {
    Lexer: undefined,
    ParserRules: [
    {"name": "row", "symbols": ["datetime", "_", "protocol", "_", "from", "_", {"literal":">"}, "_", "to", {"literal":":"}, "_", "body_message", "NL"], "postprocess": function(d) { return { datetime: d[0], protocol: d[2], from: d[4], to: d[8], body_message: d[11] }; }},
    {"name": "datetime", "symbols": ["INT", {"literal":":"}, "INT", {"literal":":"}, "INT", {"literal":"."}, "INT"], "postprocess": d => readTime(d)},
    {"name": "protocol", "symbols": ["ALNUM"], "postprocess": d => readProtocol(d)},
    {"name": "from$ebnf$1$subexpression$1", "symbols": ["MACHINE", {"literal":"."}]},
    {"name": "from$ebnf$1", "symbols": ["from$ebnf$1$subexpression$1"]},
    {"name": "from$ebnf$1$subexpression$2", "symbols": ["MACHINE", {"literal":"."}]},
    {"name": "from$ebnf$1", "symbols": ["from$ebnf$1", "from$ebnf$1$subexpression$2"], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "from", "symbols": ["from$ebnf$1", "ALNUM"], "postprocess": d => readNameFrom(d)},
    {"name": "to$ebnf$1$subexpression$1", "symbols": ["MACHINE", {"literal":"."}]},
    {"name": "to$ebnf$1", "symbols": ["to$ebnf$1$subexpression$1"]},
    {"name": "to$ebnf$1$subexpression$2", "symbols": ["MACHINE", {"literal":"."}]},
    {"name": "to$ebnf$1", "symbols": ["to$ebnf$1", "to$ebnf$1$subexpression$2"], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "to", "symbols": ["to$ebnf$1", "ALNUM"], "postprocess": d => readNameTo(d)},
    {"name": "body_message", "symbols": ["ASC"], "postprocess": d => null},
    {"name": "INT$ebnf$1", "symbols": [/[0-9]/]},
    {"name": "INT$ebnf$1", "symbols": ["INT$ebnf$1", /[0-9]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "INT", "symbols": ["INT$ebnf$1"], "postprocess": d => d.join('')},
    {"name": "ALPHA$ebnf$1", "symbols": [/[a-zA-Z]/]},
    {"name": "ALPHA$ebnf$1", "symbols": ["ALPHA$ebnf$1", /[a-zA-Z]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "ALPHA", "symbols": ["ALPHA$ebnf$1"], "postprocess": d => d.join('')},
    {"name": "ALNUM$ebnf$1", "symbols": [/[a-zA-Z0-9]/]},
    {"name": "ALNUM$ebnf$1", "symbols": ["ALNUM$ebnf$1", /[a-zA-Z0-9]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "ALNUM", "symbols": ["ALNUM$ebnf$1"], "postprocess": d => d.join('')},
    {"name": "HEX$ebnf$1", "symbols": [/[a-fA-F0-9]/]},
    {"name": "HEX$ebnf$1", "symbols": ["HEX$ebnf$1", /[a-fA-F0-9]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "HEX", "symbols": ["HEX$ebnf$1"], "postprocess": d => d.join('')},
    {"name": "ASC$ebnf$1", "symbols": [/[\x20-\x7F]/]},
    {"name": "ASC$ebnf$1", "symbols": ["ASC$ebnf$1", /[\x20-\x7F]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "ASC", "symbols": ["ASC$ebnf$1"], "postprocess": d => d.join('')},
    {"name": "MACHINE$ebnf$1", "symbols": [/[0-9a-zA-Z\-\_\#]/]},
    {"name": "MACHINE$ebnf$1", "symbols": ["MACHINE$ebnf$1", /[0-9a-zA-Z\-\_\#]/], "postprocess": function arrpush(d) {return d[0].concat([d[1]]);}},
    {"name": "MACHINE", "symbols": ["MACHINE$ebnf$1"], "postprocess": d => d.join('')},
    {"name": "NL", "symbols": ["NL"]},
    {"name": "NL", "symbols": [{"literal":"\n"}, {"literal":"\r"}]},
    {"name": "NL", "symbols": [{"literal":"\r"}, {"literal":"\n"}], "postprocess": d => function() { return null }},
    {"name": "_", "symbols": []},
    {"name": "_", "symbols": ["_", /[\s\t]/], "postprocess": d => function() { return null }}
]
  , ParserStart: "row"
}
if (typeof module !== 'undefined'&& typeof module.exports !== 'undefined') {
   module.exports = grammar;
} else {
   window.grammar = grammar;
}
})();
