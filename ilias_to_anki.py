#! /usr/bin/python3
# ilias_to_anki.py
# Converts MC questions from ILIAS result sites to Anki-importable CSV files.
# Author: Josua Zbinden - https://github.com/zjosua
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
import argparse
import bs4
import logging
import re
import sys


class mcKprim:
    """Represents a multiple choice question of the Kprim type."""
    def __init__(self, id):
        self.id = id
        self.title = ""
        self.qtext = ""
        self.options = []
        self.answers = []
        self.sources = ""
        self.extra1 = ""


class mcA:
    """Represents a multiple choice question of the A type."""
    def __init__(self, id):
        self.id = id
        self.title = ""
        self.qtext = ""
        self.options = []
        self.answers = []
        self.sources = ""
        self.extra1 = ""


class mcMultipleChoice:
    """Represents a multiple choice question of the MultipleChoice type."""
    def __init__(self, id):
        self.id = id
        self.title = ""
        self.qtext = ""
        self.options = []
        self.answers = []
        self.sources = ""
        self.extra1 = ""


# configure logging
logging.basicConfig(level=logging.INFO, filename="ilias_to_anki.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")

# configure argparse
parser = argparse.ArgumentParser(description="Convert MC questions from "
                                 + "ILIAS result sites to Anki-importable "
                                 + "CSV files.")
parser.add_argument("inputfile", action="store", metavar="file",
                    type=str, help="path to html file of the ILIAS "
                    + "results site")
parser.add_argument("-t", "--tags", help="tags to add to all notes",
                    default="", type=str, action="store")
args = parser.parse_args()

try:
    logging.debug("Opening file...")
    with open(args.inputfile, "r") as f:
        logging.debug("Done.")
        logging.debug("Parsing html...")
        soup = bs4.BeautifulSoup(f, "html.parser")
        logging.debug("Done.")
except FileNotFoundError as err:
    logging.error("File " + args.inputfile + " not found.")
    print(str(err))
    sys.exit(1)

# find Kprim type multiple choice questions
kprim_html_tags = soup.select(".solution .ilc_question_KprimChoice")
for i in range(len(kprim_html_tags)):
    for parent in kprim_html_tags[i].parents:
        if parent.get("class") and "pdfContent" in parent.get("class"):
            kprim_html_tags[i] = parent
logging.debug("Found " + str(len(kprim_html_tags)) + " Kprim type questions.")

# get question ids and create mcKprim objects
idregex = re.compile(r"\[ID: (\d+)\]")
kprim_questions = []
for i in range(len(kprim_html_tags)):
    title_tag = kprim_html_tags[i].find(class_="questionTitle")
    mo = idregex.search(title_tag.get_text())
    id = int(mo.groups()[0])
    kprim_questions.append(mcKprim(id))

# get question titles
titleregex = re.compile(r"^\d+\. +(.*) +\[")
for i in range(len(kprim_html_tags)):
    title_tag = kprim_html_tags[i].find(class_="questionTitle")
    mo = titleregex.search(title_tag.get_text())
    kprim_questions[i].title = mo.groups()[0].strip()

# get question text
for i in range(len(kprim_html_tags)):
    question_tag = kprim_html_tags[i].find(class_="ilc_qtitle_Title")
    qtext = question_tag.get_text()
    kprim_questions[i].qtext = qtext.strip()

# get answer options
optionsregex = re.compile(r"(\n|\t)*(.*)(\n|\t)*")
for i in range(len(kprim_html_tags)):
    optiontext_tags = kprim_html_tags[i].select(".solution .col-sm-6")
    for j in range(len(optiontext_tags)):
        mo = optionsregex.search(optiontext_tags[j].get_text())
        kprim_questions[i].options.append(mo.groups()[1])
    while len(kprim_questions[i].options) < 4:
        kprim_questions[i].options.append("")

# get answers
for i in range(len(kprim_html_tags)):
    option_tags = kprim_html_tags[i].select(".solution .ilc_qanswer_Answer")
    del option_tags[0]
    for j in range(len(option_tags)):
        if option_tags[j].find_all("img")[0]["title"] == "Ausgewählt":
            kprim_questions[i].answers.append(True)
        elif option_tags[j].find_all("img")[1]["title"] == "Ausgewählt":
            kprim_questions[i].answers.append(False)

# get quiz title and write sources
quiztitle = soup.select("#il_mhead_t_focus")[0].get_text()
sourceprefix = "ILIAS, " + quiztitle
for question in kprim_questions:
    question.sources = sourceprefix + ", ID: " + str(question.id)

# get extra text
feedbackregex = re.compile(r"ilc_qfeed(w|r)_Feedback(Wrong|Right)")
for i in range(len(kprim_html_tags)):
    feedback_tag = kprim_html_tags[i].find(class_=feedbackregex)
    if feedback_tag:
        kprim_questions[i].extra1 = feedback_tag.get_text().strip()

# create CSV text
logging.debug("Creating CSV text for Kprim questions...")
newlineregex = re.compile(r"(\r|\n)")
doublequoteregex = re.compile(r'"')
kprim_csv = ""
for question in kprim_questions:
    kprim_csv += '"' + question.title + '"'
    qtextstring = newlineregex.sub("<br />", question.qtext)
    qtextstring = doublequoteregex.sub('""', qtextstring)
    kprim_csv += ',"' + newlineregex.sub("<br />", question.qtext) + '"'
    for option in question.options:
        optstring = newlineregex.sub("<br />", option)
        optstring = doublequoteregex.sub('""', optstring)
        kprim_csv += ',"' + optstring + '"'
    ansstring = ""
    for answer in question.answers:
        if answer:
            ansstring += "1 "
        else:
            ansstring += "0 "
    kprim_csv += ',"' + ansstring.strip() + '"'
    srcstring = newlineregex.sub("<br />", question.sources)
    srcstring = doublequoteregex.sub('""', srcstring)
    kprim_csv += ',"' + srcstring + '"'
    extrastring = newlineregex.sub("<br />", question.extra1)
    extrastring = doublequoteregex.sub('""', extrastring)
    kprim_csv += ',"' + extrastring + '"'
    tagstring = newlineregex.sub("<br />", args.tags.strip())
    tagstring = doublequoteregex.sub('""', tagstring)
    kprim_csv += ',"' + tagstring + '"\n'
kprim_csv = kprim_csv.strip()
logging.debug("CSV text for Kprim questions is " + str(len(kprim_csv))
              + " chars long.")

# write the file
kprimfilename = args.inputfile.strip(".html") + "_Kprim.csv"
if len(kprim_questions) > 0:
    logging.debug("Writing Kprim questions to " + kprimfilename)
    with open(kprimfilename, "w") as f:
        f.write(kprim_csv)
    logging.info("Wrote Kprim questions from " + args.inputfile + " to "
                 + kprimfilename)
    print("Wrote " + str(len(kprim_questions)) + " Kprim questions from "
          + args.inputfile + " to " + kprimfilename)

# find A type multiple choice questions
mca_html_tags = soup.select(".solution .ilc_question_SingleChoice")
for i in range(len(mca_html_tags)):
    for parent in mca_html_tags[i].parents:
        if parent.get("class") and "pdfContent" in parent.get("class"):
            mca_html_tags[i] = parent
logging.debug("Found " + str(len(mca_html_tags)) + " A type questions.")

# get question ids and create mcA objects
idregex = re.compile(r"\[ID: (\d+)\]")
a_questions = []
for i in range(len(mca_html_tags)):
    title_tag = mca_html_tags[i].find(class_="questionTitle")
    mo = idregex.search(title_tag.get_text())
    id = int(mo.groups()[0])
    a_questions.append(mcA(id))

# get question titles
titleregex = re.compile(r"^\d+\. +(.*) +\[")
for i in range(len(mca_html_tags)):
    title_tag = mca_html_tags[i].find(class_="questionTitle")
    mo = titleregex.search(title_tag.get_text())
    a_questions[i].title = mo.groups()[0].strip()

# get question text
for i in range(len(mca_html_tags)):
    question_tag = mca_html_tags[i].find(class_="ilc_qtitle_Title")
    qtext = question_tag.get_text()
    a_questions[i].qtext = qtext.strip()

# get answer options
optionsregex = re.compile(r"(\n|\t)*(.*)(\n|\t)*")
for i in range(len(mca_html_tags)):
    optiontext_tags = mca_html_tags[i].select(".solution .answertext")
    for j in range(len(optiontext_tags)):
        mo = optionsregex.search(optiontext_tags[j].get_text())
        a_questions[i].options.append(mo.groups()[1])
    while len(a_questions[i].options) < 5:
        a_questions[i].options.append("")

# get answers
for i in range(len(mca_html_tags)):
    option_tags = mca_html_tags[i].select(".solution .ilc_qanswer_Answer")
    for j in range(len(option_tags)):
        if option_tags[j].find("img")["title"] == "Ausgewählt":
            a_questions[i].answers.append(True)
        elif option_tags[j].find("img")["title"] == "Nicht ausgewählt":
            a_questions[i].answers.append(False)

# get quiz title and write sources
quiztitle = soup.select("#il_mhead_t_focus")[0].get_text()
sourceprefix = "ILIAS, " + quiztitle
for question in a_questions:
    question.sources = sourceprefix + ", ID: " + str(question.id)

# get extra text
feedbackregex = re.compile(r"ilc_qfeed(w|r)_Feedback(Wrong|Right)")
for i in range(len(mca_html_tags)):
    feedback_tag = mca_html_tags[i].find(class_=feedbackregex)
    if feedback_tag:
        a_questions[i].extra1 = feedback_tag.get_text().strip()

# create CSV text
logging.debug("Creating CSV text for A questions...")
newlineregex = re.compile(r"(\r|\n)")
doublequoteregex = re.compile(r'"')
a_csv = ""
for question in a_questions:
    a_csv += '"' + question.title + '"'
    qtextstring = newlineregex.sub("<br />", question.qtext)
    qtextstring = doublequoteregex.sub('""', qtextstring)
    a_csv += ',"' + newlineregex.sub("<br />", question.qtext) + '"'
    for option in question.options:
        optstring = newlineregex.sub("<br />", option)
        optstring = doublequoteregex.sub('""', optstring)
        a_csv += ',"' + optstring + '"'
    ansstring = ""
    for answer in question.answers:
        if answer:
            ansstring += "1 "
        else:
            ansstring += "0 "
    a_csv += ',"' + ansstring.strip() + '"'
    srcstring = newlineregex.sub("<br />", question.sources)
    srcstring = doublequoteregex.sub('""', srcstring)
    a_csv += ',"' + srcstring + '"'
    extrastring = newlineregex.sub("<br />", question.extra1)
    extrastring = doublequoteregex.sub('""', extrastring)
    a_csv += ',"' + extrastring + '"'
    tagstring = newlineregex.sub("<br />", args.tags.strip())
    tagstring = doublequoteregex.sub('""', tagstring)
    a_csv += ',"' + tagstring + '"\n'
a_csv = a_csv.strip()
logging.debug("CSV text for A questions is " + str(len(a_csv))
              + " chars long.")

# write the file
mca_filename = args.inputfile.strip(".html") + "_A.csv"
if len(a_questions) > 0:
    logging.debug("Writing A questions to " + mca_filename)
    with open(mca_filename, "w") as f:
        f.write(a_csv)
    logging.info("Wrote A questions from " + args.inputfile + " to "
                 + mca_filename)
    print("Wrote " + str(len(a_questions)) + " A questions from "
          + args.inputfile + " to " + mca_filename)

# find MultpileChoice type multiple choice questions
mcmc_html_tags = soup.select(".solution .ilc_question_MultipleChoice")
for i in range(len(mcmc_html_tags)):
    for parent in mcmc_html_tags[i].parents:
        if parent.get("class") and "pdfContent" in parent.get("class"):
            mcmc_html_tags[i] = parent
logging.debug("Found " + str(len(mcmc_html_tags)) + " MC type questions.")

# get question ids and create mcA objects
idregex = re.compile(r"\[ID: (\d+)\]")
mc_questions = []
for i in range(len(mcmc_html_tags)):
    title_tag = mcmc_html_tags[i].find(class_="questionTitle")
    mo = idregex.search(title_tag.get_text())
    id = int(mo.groups()[0])
    mc_questions.append(mcA(id))

# get question titles
titleregex = re.compile(r"^\d+\. +(.*) +\[")
for i in range(len(mcmc_html_tags)):
    title_tag = mcmc_html_tags[i].find(class_="questionTitle")
    mo = titleregex.search(title_tag.get_text())
    mc_questions[i].title = mo.groups()[0].strip()

# get question text
for i in range(len(mcmc_html_tags)):
    question_tag = mcmc_html_tags[i].find(class_="ilc_qtitle_Title")
    qtext = question_tag.get_text()
    mc_questions[i].qtext = qtext.strip()

# get answer options
optionsregex = re.compile(r"(\n|\t)*(.*)(\n|\t)*")
for i in range(len(mcmc_html_tags)):
    optiontext_tags = mcmc_html_tags[i].select(".solution .answertext")
    for j in range(len(optiontext_tags)):
        mo = optionsregex.search(optiontext_tags[j].get_text())
        mc_questions[i].options.append(mo.groups()[1])
    while len(mc_questions[i].options) < 5:
        mc_questions[i].options.append("")

# get answers
for i in range(len(mcmc_html_tags)):
    option_tags = mcmc_html_tags[i].select(".solution .ilc_qanswer_Answer")
    for j in range(len(option_tags)):
        if option_tags[j].find("img")["title"] == "Ausgewählt":
            mc_questions[i].answers.append(True)
        elif option_tags[j].find("img")["title"] == "Nicht ausgewählt":
            mc_questions[i].answers.append(False)

# get quiz title and write sources
quiztitle = soup.select("#il_mhead_t_focus")[0].get_text()
sourceprefix = "ILIAS, " + quiztitle
for question in mc_questions:
    question.sources = sourceprefix + ", ID: " + str(question.id)

# get extra text
feedbackregex = re.compile(r"ilc_qfeed(w|r)_Feedback(Wrong|Right)")
for i in range(len(mcmc_html_tags)):
    feedback_tag = mcmc_html_tags[i].find(class_=feedbackregex)
    if feedback_tag:
        mc_questions[i].extra1 = feedback_tag.get_text().strip()

# create CSV text
logging.debug("Creating CSV text for MC questions...")
newlineregex = re.compile(r"(\r|\n)")
doublequoteregex = re.compile(r'"')
mc_csv = ""
for question in mc_questions:
    mc_csv += '"' + question.title + '"'
    qtextstring = newlineregex.sub("<br />", question.qtext)
    qtextstring = doublequoteregex.sub('""', qtextstring)
    mc_csv += ',"' + newlineregex.sub("<br />", question.qtext) + '"'
    for option in question.options:
        optstring = newlineregex.sub("<br />", option)
        optstring = doublequoteregex.sub('""', optstring)
        mc_csv += ',"' + optstring + '"'
    ansstring = ""
    for answer in question.answers:
        if answer:
            ansstring += "1 "
        else:
            ansstring += "0 "
    mc_csv += ',"' + ansstring.strip() + '"'
    srcstring = newlineregex.sub("<br />", question.sources)
    srcstring = doublequoteregex.sub('""', srcstring)
    mc_csv += ',"' + srcstring + '"'
    extrastring = newlineregex.sub("<br />", question.extra1)
    extrastring = doublequoteregex.sub('""', extrastring)
    mc_csv += ',"' + extrastring + '"'
    tagstring = newlineregex.sub("<br />", args.tags.strip())
    tagstring = doublequoteregex.sub('""', tagstring)
    mc_csv += ',"' + tagstring + '"\n'
mc_csv = mc_csv.strip()
logging.debug("CSV text for MC questions is " + str(len(mc_csv))
              + " chars long.")

# write the file
mcmc_filename = args.inputfile.strip(".html") + "_MC.csv"
if len(mc_questions) > 0:
    logging.debug("Writing MC questions to " + mcmc_filename)
    with open(mcmc_filename, "w") as f:
        f.write(mc_csv)
    logging.info("Wrote MC questions from " + args.inputfile + " to "
                 + mcmc_filename)
    print("Wrote " + str(len(mc_questions)) + " MC questions from "
          + args.inputfile + " to " + mcmc_filename)
