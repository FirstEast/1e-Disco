this["com"] = this["com"] || {};
this["com"]["firsteast"] = this["com"]["firsteast"] || {};
this["com"]["firsteast"]["templates"] = this["com"]["firsteast"]["templates"] || {};

this["com"]["firsteast"]["templates"]["device-preview"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  
  return "\n    <div class=\"mock-label\">MOCK</div>\n  ";
  }

function program3(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n<div class=\"selector-area\">\n    <b>Saved:</b> <select class=\"saved-patterns\">\n      <optgroup label=\"Party Worthy\">\n        ";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.partyWorthySavedPatterns), {hash:{},inverse:self.noop,fn:self.program(4, program4, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n      </optgroup>\n      <optgroup label=\"Non Party Worthy\">\n        ";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.nonPartyWorthySavedPatterns), {hash:{},inverse:self.noop,fn:self.program(4, program4, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n      </optgroup>\n    </select>\n    <b>Builders:</b> <select class=\"class-patterns\">\n      ";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.patterns), {hash:{},inverse:self.noop,fn:self.program(6, program6, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    </select>\n    <div class=\"params\">\n      ";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.parameters), {hash:{},inverse:self.noop,fn:self.programWithDepth(8, program8, data, depth0),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    </div>\n    <br>\n    <span>Party Worthy</span><input type=checkbox class=\"party-worthy-input\" ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.partyWorthy), {hash:{},inverse:self.noop,fn:self.program(10, program10, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "></input>\n    <br>\n    <input type=text class=\"save-name-input\"></input>\n    <button class=\"save-button\">Save Pattern</button>\n</div>\n";
  return buffer;
  }
function program4(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n          <option value=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.attributes)),stack1 == null || stack1 === false ? stack1 : stack1.saveName)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.attributes)),stack1 == null || stack1 === false ? stack1 : stack1.saveName)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</option>\n        ";
  return buffer;
  }

function program6(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n      <option value=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.attributes)),stack1 == null || stack1 === false ? stack1 : stack1.name)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.attributes)),stack1 == null || stack1 === false ? stack1 : stack1.name)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</option>\n      ";
  return buffer;
  }

function program8(depth0,data,depth1) {
  
  var buffer = "", stack1, helper;
  buffer += "\n        <div class=\"param\">\n          <span>";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + ": </span>\n          ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.type), {hash:{},inverse:self.programWithDepth(12, program12, data, depth1),fn:self.program(9, program9, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n        </div>\n      ";
  return buffer;
  }
function program9(depth0,data) {
  
  var buffer = "", stack1, helper;
  buffer += "\n            <input class=\"param-input\" type=\"";
  if (helper = helpers.type) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.type); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\" value=\"";
  if (helper = helpers.val) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.val); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\" name=\"";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\" ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.val), {hash:{},inverse:self.noop,fn:self.program(10, program10, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "></input>\n          ";
  return buffer;
  }
function program10(depth0,data) {
  
  
  return "checked=\"checked\"";
  }

function program12(depth0,data,depth2) {
  
  var buffer = "", stack1;
  buffer += "\n            ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.pattern), {hash:{},inverse:self.noop,fn:self.programWithDepth(13, program13, data, depth2),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n            ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.gif), {hash:{},inverse:self.noop,fn:self.programWithDepth(16, program16, data, depth2),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n            ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.image), {hash:{},inverse:self.noop,fn:self.programWithDepth(19, program19, data, depth2),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n          ";
  return buffer;
  }
function program13(depth0,data,depth3) {
  
  var buffer = "", stack1, helper;
  buffer += "\n            <select class=\"param-input\" name=\"";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\" data-type=\"pattern\">\n              ";
  stack1 = helpers.each.call(depth0, (depth3 && depth3.savedPatterns), {hash:{},inverse:self.noop,fn:self.program(14, program14, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n            </select>\n            ";
  return buffer;
  }
function program14(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n              <option value=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.attributes)),stack1 == null || stack1 === false ? stack1 : stack1.saveName)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.attributes)),stack1 == null || stack1 === false ? stack1 : stack1.saveName)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</option>\n              ";
  return buffer;
  }

function program16(depth0,data,depth3) {
  
  var buffer = "", stack1, helper;
  buffer += "\n            <select class=\"param-input\" name=\"";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\" data-type=\"gif\">\n              ";
  stack1 = helpers.each.call(depth0, (depth3 && depth3.gifList), {hash:{},inverse:self.noop,fn:self.program(17, program17, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n            </select>\n            ";
  return buffer;
  }
function program17(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n              <option value=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.attributes)),stack1 == null || stack1 === false ? stack1 : stack1.name)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.attributes)),stack1 == null || stack1 === false ? stack1 : stack1.name)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</option>\n              ";
  return buffer;
  }

function program19(depth0,data,depth3) {
  
  var buffer = "", stack1, helper;
  buffer += "\n            <select class=\"param-input\" name=\"";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\" data-type=\"image\">\n              ";
  stack1 = helpers.each.call(depth0, (depth3 && depth3.imageList), {hash:{},inverse:self.noop,fn:self.program(17, program17, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n            </select>\n            ";
  return buffer;
  }

  buffer += "<div class=\"preview-view\">\n  ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.isMock), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  <div class=\"expander\">E</div>\n</div>\n";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.showEdit), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n";
  return buffer;
  });

this["com"]["firsteast"]["templates"]["nav-bar"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<div class=\"logo\"></div>\n<div class=\"title\">\n  1E Disco System Control\n</div>";
  });

this["com"]["firsteast"]["templates"]["side-menu"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  
  return "checked=\"checked\"";
  }

function program3(depth0,data,depth1) {
  
  var buffer = "", stack1;
  buffer += "\n      "
    + escapeExpression(((stack1 = (data == null || data === false ? data : data.key)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + ":\n      <select class=\"hotkey-patterns\" data-key=\""
    + escapeExpression(((stack1 = (data == null || data === false ? data : data.key)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n        <optgroup label=\"Party Worthy\">\n          ";
  stack1 = helpers.each.call(depth0, (depth1 && depth1.partyWorthySaveModels), {hash:{},inverse:self.noop,fn:self.program(4, program4, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n        </optgroup>\n        <optgroup label=\"Non Party Worthy\">\n          ";
  stack1 = helpers.each.call(depth0, (depth1 && depth1.nonPartyWorthySaveModels), {hash:{},inverse:self.noop,fn:self.program(4, program4, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n        </optgroup>\n      </select>\n    ";
  return buffer;
  }
function program4(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n            <option value=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.attributes)),stack1 == null || stack1 === false ? stack1 : stack1.saveName)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.attributes)),stack1 == null || stack1 === false ? stack1 : stack1.saveName)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</option>\n          ";
  return buffer;
  }

  buffer += "<div class=\"handle\">\n  <div class=\"inner-handle\">\n    +\n  </div>\n</div>\n\n<div class=\"controls\">\n  <label>Real/Mock Control:</label>\n  <div class=\"real-mock-controls\">\n    Show Real: <input type=\"checkbox\" class=\"menu-check show-real\" ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.displayAttrs)),stack1 == null || stack1 === false ? stack1 : stack1.showReal), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "></input>\n    <br/>\n    Show Mock: <input type=\"checkbox\" class=\"menu-check show-mock\" ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.displayAttrs)),stack1 == null || stack1 === false ? stack1 : stack1.showMock), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "></input>\n    <br/>\n    <button class=\"swap-mock-real\">Copy Mock Patterns to Real</button>\n    <button class=\"swap-real-mock\">Copy Real Patterns to Mock</button>\n  </div>\n  <br>\n  <label>Hotkeys:</label>\n  <div class=\"hotkeys\">\n    ";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.hotkeySet), {hash:{},inverse:self.noop,fn:self.programWithDepth(3, program3, data, depth0),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  </div>\n</div>";
  return buffer;
  });