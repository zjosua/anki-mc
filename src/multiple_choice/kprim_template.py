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
	var solutions = document.getElementById("MC_solutions").innerHTML;
	solutions = solutions.split(" ");
	for (i = 0; i < solutions.length; i++) {
		solutions[i] = Number(solutions[i]);
	}

	var output = document.getElementById("output");

	var qrows = document.getElementById("qtable").getElementsByTagName("tr");

	var qanda = new Array();

	for (i = 0; i < qrows.length - 1; i++) {
		qanda[i] = new Object();
		qanda[i].question = qrows[i+1].getElementsByTagName("td")[2].innerHTML;
		qanda[i].answer = solutions[i];
	}

	qanda = shuffle(qanda);

	var mc_solutions = new String();

	for (i = 0; i < qrows.length - 1; i++) {
		qrows[i+1].getElementsByTagName("td")[2].innerHTML = qanda[i].question;
		solutions[i] = qanda[i].answer;
		mc_solutions += qanda[i].answer + " ";
	}
	mc_solutions = mc_solutions.substring(0, mc_solutions.lastIndexOf(" "));
	document.getElementById("MC_solutions").innerHTML = mc_solutions;

	document.getElementById("qtable").HTML = qrows;

	sendStuff();
}

function onCheck() {
	var qrows = document.getElementById("qtable").getElementsByTagName("tr");
	document.getElementById("user_answers").innerHTML = "";

	for (i = 0; i < qrows.length - 1; i++) {
		if (qrows[i+1].getElementsByTagName("td")[0].getElementsByTagName("input")[0].checked) {
			document.getElementById("user_answers").innerHTML += "1 ";
		} else if (qrows[i+1].getElementsByTagName("td")[1].getElementsByTagName("input")[0].checked) {
			document.getElementById("user_answers").innerHTML += "0 ";
		} else {
			document.getElementById("user_answers").innerHTML += "- ";
		}
	}
	document.getElementById("user_answers").innerHTML = document.getElementById("user_answers").innerHTML.trim();

	sendStuff();
}

function sendStuff() {
	msg = "mc_user_sel:";
	msg += document.getElementById("user_answers").innerHTML;
	msg += ";mc_soultions:";
	msg += document.getElementById("MC_solutions").innerHTML;
	msg += ";qtable:";
	msg += document.getElementById("qtable").outerHTML;
	msg += ";;";
	pycmd(msg);
}

/*
The following block is from Glutanimate's Cloze Overlapper card template.
The Cloze Overlapper card template is licensed under the CC BY-SA 4.0
license (https://creativecommons.org/licenses/by-sa/4.0/).
*/
if (document.readyState === "complete") {
	setTimeout(onShuffle, 1);
} else {
	document.addEventListener("DOMContentLoaded", function() {
		setTimeout(onShuffle, 1);
	}, false);
}
</script>

{{#Title}}<h3>{{Title}}<br /></h3>{{/Title}}
{{#Question}}<p>{{Question}}</p>{{/Question}}
<form>
	<table style="boder: 1px solid black" id="qtable">
		<tbody>
			<tr>
				<th>yes</th><th>no</th><th></th>
			</tr>
			{{#MC_1}}<tr>
				<td onInput="onCheck()" style="text-align: center"><input name="ans_1" type="radio" value="1"></td>
				<td onInput="onCheck()" style="text-align: center"><input name="ans_1" type="radio" value="0"></td>
				<td>{{MC_1}}</td>
			</tr>{{/MC_1}}
			{{#MC_2}}<tr>
				<td onInput="onCheck()" style="text-align: center"><input name="ans_2" type="radio" value="1"></td>
				<td onInput="onCheck()" style="text-align: center"><input name="ans_2" type="radio" value="0"></td>
				<td>{{MC_2}}</td>
			</tr>{{/MC_2}}
			{{#MC_3}}<tr>
				<td onInput="onCheck()" style="text-align: center"><input name="ans_3" type="radio" value="1"></td>
				<td onInput="onCheck()" style="text-align: center"><input name="ans_3" type="radio" value="0"></td>
				<td>{{MC_3}}</td>
			</tr>{{/MC_3}}
			{{#MC_4}}<tr>
				<td onInput="onCheck()" style="text-align: center"><input name="ans_4" type="radio" value="1"></td>
				<td onInput="onCheck()" style="text-align: center"><input name="ans_4" type="radio" value="0"></td>
				<td>{{MC_4}}</td>
			</tr>{{/MC_4}}
		</tbody>
	</table>
</form>
<div class="hidden" id="MC_solutions">{{Answers}}</div>
<div class="hidden" id="user_answers">- - - -</div>\
"""

card_back = """\
<script>
function onLoad() {
	var solutions = document.getElementById("MC_solutions").innerHTML;
	solutions = solutions.split(" ");
	for (i = 0; i < solutions.length; i++) {
		solutions[i] = Number(solutions[i]);
	}

	var answers = document.getElementById("user_answers").innerHTML;
	answers = answers.split(" ");
	for (i = 0; i < answers.length; i++) {
		answers[i] = Number(answers[i]);
	}

	var output = document.getElementById("output");

	var atable = document.getElementById("qtable").cloneNode(true);
	atable.setAttribute("id", "atable");
	output.innerHTML = "<hr id='answer' /><br />" + atable.outerHTML;

	var qrows = document.getElementById("qtable").getElementsByTagName("tr");

	for (i = 0; i < answers.length; i++) {
		//Set the radio buttons in the qtable.
		qrows[i+1].getElementsByTagName("td")[answers[i] ? 0 : 1].getElementsByTagName("input")[0].checked = true;
		//Colorize the qtable.
		if (solutions[i] && answers[i]) {
			qrows[i+1].setAttribute("class", "correct");
		} else if (!solutions[i] && !answers[i]){
			qrows[i+1].setAttribute("class", "correct");
		} else {
			qrows[i+1].setAttribute("class", "wrong");
		}
	}

	var arows = document.getElementById("atable").getElementsByTagName("tr");

	for (i = 0; i < solutions.length; i++) {
		//Rename the radio buttons of the atable to avoid interference with those in the qtable.
		arows[i+1].getElementsByTagName("td")[0].getElementsByTagName("input")[0].setAttribute("name", "solution_" + String(i+1));
		arows[i+1].getElementsByTagName("td")[1].getElementsByTagName("input")[0].setAttribute("name", "solution_" + String(i+1));
		//Set the radio buttons in the atable.
		arows[i+1].getElementsByTagName("td")[solutions[i] ? 0 : 1].getElementsByTagName("input")[0].checked = true;
	}
}

/*
The following block is from Glutanimate's Cloze Overlapper card template.
The Cloze Overlapper card template is licensed under the CC BY-SA 4.0
license (https://creativecommons.org/licenses/by-sa/4.0/).
*/
if (document.readyState === "complete") {
	setTimeout(onLoad, 1);
} else {
	document.addEventListener("DOMContentLoaded", function() {
		setTimeout(onLoad, 1);
	}, false);
}
</script>

{{#Title}}<h3 id="myH1">{{Title}}</h3>{{/Title}}
{{#Question}}<p>{{Question}}</p>{{/Question}}
qtable_here
<p id="output"></p>
<div class="hidden" id="MC_solutions">solutions_here</div>
<div class="hidden" id="user_answers">user_answers_here</div>
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
 border: 1px solid black;
 border-collapse: collapse;
 padding: 5px;
}

.nightMode table, td, th {
 border-color: white;
}

.correct {
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

kprim_model = "Kprim"
kprim_card = "Kprim"
kprim_fields = {
    "title": "Title",
    "question": "Question",
    "mc1": "MC_1",
    "mc2": "MC_2",
    "mc3": "MC_3",
    "mc4": "MC_4",
    "answers": "Answers",
    "sources": "Sources",
    "extra": "Extra 1"
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

def initializeKprimModels():
    model = mw.col.models.byName(kprim_model)
    if not model:
        model = addModel(mw.col)
