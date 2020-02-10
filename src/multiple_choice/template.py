# Multiple Choice for Anki
#
# Copyright (C) 2018-2020  zjosua <https://github.com/zjosua>
#
# This file is based on template.py from Glutanimate's
# Cloze Overlapper Add-on for Anki
#
# Copyright (C)  2016-2019 Aristotelis P. <https://glutanimate.com/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License that
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.

"""
Manages note type and templates
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from anki.consts import MODEL_STD

from aqt import mw

card_front = """\
<script>
    // Loading Persistence
    // https://github.com/SimonLammer/anki-persistence
    // v0.5.2 - https://github.com/SimonLammer/anki-persistence/blob/62463a7f63e79ce12f7a622a8ca0beb4c1c5d556/script.js
    if (void 0 === window.Persistence) { var _persistenceKey = "github.com/SimonLammer/anki-persistence/", _defaultKey = "_default"; if (window.Persistence_sessionStorage = function () { var e = !1; try { "object" == typeof window.sessionStorage && (e = !0, this.clear = function () { for (var e = 0; e < sessionStorage.length; e++) { var t = sessionStorage.key(e); 0 == t.indexOf(_persistenceKey) && (sessionStorage.removeItem(t), e--) } }, this.setItem = function (e, t) { void 0 == t && (t = e, e = _defaultKey), sessionStorage.setItem(_persistenceKey + e, JSON.stringify(t)) }, this.getItem = function (e) { return void 0 == e && (e = _defaultKey), JSON.parse(sessionStorage.getItem(_persistenceKey + e)) }, this.removeItem = function (e) { void 0 == e && (e = _defaultKey), sessionStorage.removeItem(_persistenceKey + e) }) } catch (e) { } this.isAvailable = function () { return e } }, window.Persistence_windowKey = function (e) { var t = window[e], i = !1; "object" == typeof t && (i = !0, this.clear = function () { t[_persistenceKey] = {} }, this.setItem = function (e, i) { void 0 == i && (i = e, e = _defaultKey), t[_persistenceKey][e] = i }, this.getItem = function (e) { return void 0 == e && (e = _defaultKey), t[_persistenceKey][e] || null }, this.removeItem = function (e) { void 0 == e && (e = _defaultKey), delete t[_persistenceKey][e] }, void 0 == t[_persistenceKey] && this.clear()), this.isAvailable = function () { return i } }, window.Persistence = new Persistence_sessionStorage, Persistence.isAvailable() || (window.Persistence = new Persistence_windowKey("py")), !Persistence.isAvailable()) { var titleStartIndex = window.location.toString().indexOf("title"), titleContentIndex = window.location.toString().indexOf("main", titleStartIndex); titleStartIndex > 0 && titleContentIndex > 0 && titleContentIndex - titleStartIndex < 10 && (window.Persistence = new Persistence_windowKey("qt")) } }
</script>

<script>

    // Generate the table depending on the type.

    function generateTable() {
        var type = document.getElementById("Card_Type").innerHTML;
        var table = document.createElement("table");
        var tbody = document.createElement("tbody");
        for (var i = 0; i < 5; i++) {
            if (type == 0 && i == 0) {
                tbody.innerHTML = tbody.innerHTML + '<tr><th>yes</th><th>no</th><th></th></tr>';
            }

            if (document.getElementById('Q_' + (i + 1)).innerHTML != '') {
                var html = [];

                html.push('<tr>');
                for (var j = 0; j < ((type == 0) ? 2 : 1); j++) {
                    html.push(
                        '<td onInput="onCheck()" style="text-align: center"><input name="ans_' + ((type != 2) ? (i + 1) : 'A') + '" type="' +
                        ((type == 1) ? 'checkbox' : 'radio') + '" value="' + ((j == 0) ? 1 : 0) + '"></td>');
                }
                html.push('<td>' + document.getElementById('Q_' + (i + 1)).innerHTML + '</td>')
                html.push('</tr>');
                tbody.innerHTML = tbody.innerHTML + html.join("");
            }

        }

        table.appendChild(tbody);
        document.getElementById('qtable').innerHTML = table.innerHTML;
        onShuffle();
    }

    function shuffle(array) {
        var currentIndex = array.length, temporaryValue, randomIndex;

        // While there remain elements to shuffle...
        while (0 !== currentIndex) {

            // Pick a remaining element...
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex -= 1;

            // And swap it with the current element.
            temporaryValue = array[currentIndex];
            array[currentIndex] = array[randomIndex];
            array[randomIndex] = temporaryValue;
        }

        return array;
    }

    function onShuffle() {
        var solutions = document.getElementById("Q_solutions").innerHTML;
        solutions = solutions.split(" ");
        for (i = 0; i < solutions.length; i++) {
            solutions[i] = Number(solutions[i]);
        }

        var output = document.getElementById("output");

        var qrows = document.getElementById("qtable").getElementsByTagName("tr");

        var qanda = new Array();

        var type = document.getElementById("Card_Type").innerHTML;

        for (i = 0; i < ((type == 0) ? qrows.length - 1 : qrows.length); i++) {
            qanda[i] = new Object();
            qanda[i].question = qrows[(type == 0) ? i + 1 : i].getElementsByTagName("td")[(type == 0) ? 2 : 1].innerHTML;
            qanda[i].answer = solutions[i];
        }

        qanda = shuffle(qanda);

        var mc_solutions = new String();

        for (i = 0; i < ((type == 0) ? qrows.length - 1 : qrows.length); i++) {
            qrows[(type == 0) ? i + 1 : i].getElementsByTagName("td")[(type == 0) ? 2 : 1].innerHTML = qanda[i].question;
            solutions[i] = qanda[i].answer;
            mc_solutions += qanda[i].answer + " ";
        }
        mc_solutions = mc_solutions.substring(0, mc_solutions.lastIndexOf(" "));
        document.getElementById("Q_solutions").innerHTML = mc_solutions;

        document.getElementById("qtable").HTML = qrows;
    }

    function onCheck() {
        // Generate user_answers
        var type = document.getElementById("Card_Type").innerHTML;
        var qrows = document.getElementById("qtable").getElementsByTagName('tbody')[0].getElementsByTagName("tr");
        document.getElementById("user_answers").innerHTML = "";
        for (i = 0; i < ((type == 0) ? qrows.length - 1 : qrows.length); i++) {
            var j;
            if (type == 0) {
                j = i + 1;
            } else j = i;
            if (qrows[j].getElementsByTagName("td")[0].getElementsByTagName("input")[0].checked) {

                document.getElementById("user_answers").innerHTML += "1 ";
            } else if (type != 0 && !qrows[j].getElementsByTagName("td")[(type == 0) ? 1 : 0].getElementsByTagName("input")[0].checked) {
                document.getElementById("user_answers").innerHTML += "0 ";
            } else if (type == 0 && qrows[j].getElementsByTagName("td")[(type == 0) ? 1 : 0].getElementsByTagName("input")[0].checked) {
                document.getElementById("user_answers").innerHTML += "0 ";
            } else {
                document.getElementById("user_answers").innerHTML += "- ";
            }
        }

        document.getElementById("user_answers").innerHTML = document.getElementById("user_answers").innerHTML.trim();

        // Send Stuff to Persistence
        if (Persistence.isAvailable()) {
            Persistence.clear();
            Persistence.setItem('user_answers', document.getElementById("user_answers").innerHTML);
            Persistence.setItem('Q_solutions', document.getElementById("Q_solutions").innerHTML);
            Persistence.setItem('qtable', document.getElementById("qtable").innerHTML);
        }
    }

    /*
        The following block is from Glutanimate's Cloze Overlapper card template.
        The Cloze Overlapper card template is licensed under the CC BY-SA 4.0
        license (https://creativecommons.org/licenses/by-sa/4.0/).
    */
    if (document.readyState === "complete") {
        setTimeout(generateTable(), 1);

    } else {
        document.addEventListener("DOMContentLoaded", function () {
            setTimeout(generateTable(), 1);
        }, false);
    }
</script>

{{#Title}}<h3 id="myH1">{{Title}}</h3>{{/Title}}
{{#Question}}<p>{{Question}}</p>{{/Question}}

<table style="boder: 1px solid black" id="qtable"></table>

<div class="hidden" id="Q_solutions">{{Answers}}</div>
<div class="hidden" id="user_answers">- - - -</div>
<div class="hidden" id="Card_Type">{{QType}}</div>

<div class="hidden" id="Q_1">{{Q_1}}</div>
<div class="hidden" id="Q_2">{{Q_2}}</div>
<div class="hidden" id="Q_3">{{Q_3}}</div>
<div class="hidden" id="Q_4">{{Q_4}}</div>
<div class="hidden" id="Q_5">{{Q_5}}</div>\
"""

card_back = """\
<script>
    // Loading Persistence
    // https://github.com/SimonLammer/anki-persistence
    // v0.5.2 - https://github.com/SimonLammer/anki-persistence/blob/62463a7f63e79ce12f7a622a8ca0beb4c1c5d556/script.js
    if (void 0 === window.Persistence) { var _persistenceKey = "github.com/SimonLammer/anki-persistence/", _defaultKey = "_default"; if (window.Persistence_sessionStorage = function () { var e = !1; try { "object" == typeof window.sessionStorage && (e = !0, this.clear = function () { for (var e = 0; e < sessionStorage.length; e++) { var t = sessionStorage.key(e); 0 == t.indexOf(_persistenceKey) && (sessionStorage.removeItem(t), e--) } }, this.setItem = function (e, t) { void 0 == t && (t = e, e = _defaultKey), sessionStorage.setItem(_persistenceKey + e, JSON.stringify(t)) }, this.getItem = function (e) { return void 0 == e && (e = _defaultKey), JSON.parse(sessionStorage.getItem(_persistenceKey + e)) }, this.removeItem = function (e) { void 0 == e && (e = _defaultKey), sessionStorage.removeItem(_persistenceKey + e) }) } catch (e) { } this.isAvailable = function () { return e } }, window.Persistence_windowKey = function (e) { var t = window[e], i = !1; "object" == typeof t && (i = !0, this.clear = function () { t[_persistenceKey] = {} }, this.setItem = function (e, i) { void 0 == i && (i = e, e = _defaultKey), t[_persistenceKey][e] = i }, this.getItem = function (e) { return void 0 == e && (e = _defaultKey), t[_persistenceKey][e] || null }, this.removeItem = function (e) { void 0 == e && (e = _defaultKey), delete t[_persistenceKey][e] }, void 0 == t[_persistenceKey] && this.clear()), this.isAvailable = function () { return i } }, window.Persistence = new Persistence_sessionStorage, Persistence.isAvailable() || (window.Persistence = new Persistence_windowKey("py")), !Persistence.isAvailable()) { var titleStartIndex = window.location.toString().indexOf("title"), titleContentIndex = window.location.toString().indexOf("main", titleStartIndex); titleStartIndex > 0 && titleContentIndex > 0 && titleContentIndex - titleStartIndex < 10 && (window.Persistence = new Persistence_windowKey("qt")) } }
</script>

<script>
    function onLoad() {
        // Check if Persistence is Available
        if (Persistence.isAvailable) {
            // Parsing solutions
            solutions = Persistence.getItem('Q_solutions').split(" ");
            for (i = 0; i < solutions.length; i++) {
                solutions[i] = Number(solutions[i]);
            }
            var answers = Persistence.getItem('user_answers').split(" ");
            var type = document.getElementById('CardType').innerHTML;

            var qtable = document.getElementById('qtable');
            qtable.innerHTML = Persistence.getItem('qtable');

            var output = document.getElementById("output");

            var atable = qtable.cloneNode(true);
            atable.setAttribute("id", "atable");
            output.innerHTML = "<hr id='answer' />" + atable.outerHTML;

            document.getElementById('qtable').innerHTML = qtable.innerHTML;
            var qrows = qtable.getElementsByTagName('tbody')[0].getElementsByTagName("tr");
            
            for (i = 0; i < answers.length; i++) {
                //Set the radio buttons in the qtable.
                if (type == 0) {
                    if (answers[i] === "1") {
                        qrows[i + 1].getElementsByTagName("td")[0].getElementsByTagName("input")[0].checked = true;
                    } else if (answers[i] === "0") {
                        qrows[i + 1].getElementsByTagName("td")[1].getElementsByTagName("input")[0].checked = true;
                    }
                } else {
                    qrows[i].getElementsByTagName("td")[0].getElementsByTagName("input")[0].checked = (answers[i]==1) ? true : false;
                }
                //Colorize the qtable.
                if (solutions[i] && ((type == 0) ? answers[i] === "1" : answers[i])) {
                    qrows[(type != 0) ? i : i + 1].setAttribute("class", "correct");
                } else if (!solutions[i] && ((type == 0) ? answers[i] === "0" : !answers[i])) {
                    qrows[(type != 0) ? i : i + 1].setAttribute("class", "correct");
                } else {
                    qrows[(type != 0) ? i : i + 1].setAttribute("class", "wrong");
                }
            }
            
            var arows = document.getElementById("atable").getElementsByTagName("tbody")[0].getElementsByTagName("tr");
            for (i = 0; i < solutions.length; i++) {
                //Rename the radio buttons of the atable to avoid interference with those in the qtable.
                if (type==0) arows[i + 1].getElementsByTagName("td")[1].getElementsByTagName("input")[0].setAttribute("name", "ans_" + ((type != 2) ? String(i + 1) : 'A') + "_solution");
                             arows[(type!=0) ? i : i+1].getElementsByTagName("td")[0].getElementsByTagName("input")[0].setAttribute("name", "ans_" + ((type != 2) ? String(i + 1) : 'A') + "_solution");
                //Set the radio buttons in the atable.
                if (type==0) arows[i + 1].getElementsByTagName("td")[solutions[i] ? 0 : 1].getElementsByTagName("input")[0].checked = true;
                else arows[i].getElementsByTagName("td")[0].getElementsByTagName("input")[0].checked = solutions[i] ? true : false;
            }
            Persistence.clear();
        }
    }

    if (document.readyState === "complete") {
        setTimeout(onLoad, 1);
    } else {
        document.addEventListener("DOMContentLoaded", function () {
            setTimeout(onLoad, 1);
        }, false);
    }
</script>

{{#Title}}<h3 id="myH1">{{Title}}</h3>{{/Title}}
{{#Question}}<p>{{Question}}</p>{{/Question}}
<table id="qtable"></table>
<p id="output"></p>
<div class="hidden" id="MC_solutions">solutions_here</div>

<div class="hidden" id="user_answers">user_answers_here</div>
<div class="hidden" id="CardType">{{QType}}</div>
{{#Sources}}<p class="small" id="sources"><b>Sources:</b><br />{{Sources}}</p>{{/Sources}}
{{#Extra 1}}<p class="small" id="extra1"><b>Extra 1:</b><br />{{Extra 1}}</p>{{/Extra 1}}\
"""

card_css = """\
.card {
 font-family: arial;
 font-size: 20px;
 text-align: left;
 color: black;
 background-color: white;
}

.small {
 font-size: 15px;
}

table, td, th {
 border-collapse: collapse;
 padding: 5px;
}

.correct {
	background-color: lime;
}

.nightMode .correct {
	background-color: #009900;
}

.wrong {
	background-color: OrangeRed;
}

.hidden {
  /*
  This block is from Glutanimate's Cloze Overlapper card template.
  The Cloze Overlapper card template is licensed under the CC BY-SA 4.0
  license (https://creativecommons.org/licenses/by-sa/4.0/).
  */
  /* guarantees a consistent width across front and back */
  font-weight: bold;
  display: block;
  line-height:0;
  height: 0;
  overflow: hidden;
  visibility: hidden;
}\
"""

kprim_model = "AllInOne (kprim, mc, sc)"
kprim_card = "AllInOne (kprim, mc, sc)"
kprim_fields = {
    "question": "Question",
    "qtype": "QType (0=kprim,1=mc,2=sc)",
    "q1": "Q_1",
    "q2": "Q_2",
    "q3": "Q_3",
    "q4": "Q_4",
    "answers": "Answers",
    "sources": "Sources",
    "extra": "Extra 1"
    "title": "Title",
}

def addModel(col):
    """Add add-on note type to collection"""
    models = col.models
    model = models.new(kprim_model)
    model['type'] = MODEL_STD
    # Add fields:
    for i in kprim_fields.keys():
        fld = models.newField(kprim_fields[i])
        models.addField(model, fld)
    # Add template
    template = models.newTemplate(kprim_card)
    template['qfmt'] = card_front
    template['afmt'] = card_back
    model['css'] = card_css
    model['sortf'] = 0 # set sortfield to title
    models.addTemplate(model, template)
    models.add(model)
    return model

def updateTemplate(col):
    """Update add-on card templates"""
    print("Updating %s card template".format(kprim_model))
    model = col.models.byName(kprim_model)
    template = model['tmpls'][0]
    template['qfmt'] = card_front
    template['afmt'] = card_back
    model['css'] = card_css
    col.models.save()
    return model

def initializeModel():
    model = mw.col.models.byName(kprim_model)
    if not model:
        model = addModel(mw.col)
