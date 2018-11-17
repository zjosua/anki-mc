#! /usr/bin/python3
# iliasToAnki.py
# Converts MC questions from ILIAS result sites to Anki-importable CSV files.
# Author: Josua Zbinden - https://github.com/zjosua
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
import argparse, sys, logging, re, bs4

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

# configure logging
logging.basicConfig(level=logging.INFO, filename="iliasToAnki.log", \
    format="%(asctime)s - %(levelname)s - %(message)s")

# configure argparse
parser = argparse.ArgumentParser(description="Convert MC questions from ILIAS \
result sites to Anki-importable CSV files.")
parser.add_argument("resultFile", help="path to html file of the ILIAS \
results site", type=str, action="store", metavar="file")
parser.add_argument("-t", "--tags", help="tags to add to all notes", \
    default="", type=str, action="store")
args = parser.parse_args()

try:
    logging.debug("Opening file...")
    f = open(args.resultFile, "r")
    logging.debug("Done.")
except FileNotFoundError as err:
    logging.error("File " + args.resultFile + " not found.")
    print(str(err))
    sys.exit(1)

logging.debug("Parsing html...")
soup = bs4.BeautifulSoup(f, "html.parser")
logging.debug("Done.")
f.close()

# find Kprim type multiple choice questions
kprimHtmlTags = soup.select(".solution .ilc_question_KprimChoice")
for i in range(len(kprimHtmlTags)):
     for parent in kprimHtmlTags[i].parents:
        if parent.get("class") and "pdfContent" in parent.get("class"):
            kprimHtmlTags[i] = parent
logging.debug("Found " + str(len(kprimHtmlTags)) + " Kprim type questions.")

# get question ids and create mcKprim objects
idRegex = re.compile(r"\[ID: (\d+)\]")
kprimQuestions = []
for i in range(len(kprimHtmlTags)):
    titleTag = kprimHtmlTags[i].find(class_="questionTitle")
    mo = idRegex.search(titleTag.get_text())
    id = int(mo.groups()[0])
    kprimQuestions.append(mcKprim(id))

# get question titles
titleRegex = re.compile(r"^\d+\. +((.*)\w) +\[")
for i in range(len(kprimHtmlTags)):
    titleTag = kprimHtmlTags[i].find(class_="questionTitle")
    mo = titleRegex.search(titleTag.get_text())
    kprimQuestions[i].title = mo.groups()[0]

# get question text
for i in range(len(kprimHtmlTags)):
    questionTag = kprimHtmlTags[i].find(class_="ilc_qtitle_Title")
    qtext = questionTag.get_text()
    kprimQuestions[i].qtext = qtext.strip()

# get answer options
optionsRegex = re.compile(r"(\n|\t)*(.*)(\n|\t)*")
for i in range(len(kprimHtmlTags)):
    optiontextTags = kprimHtmlTags[i].select(".solution .col-sm-4")
    for j in range(len(optiontextTags)):
        mo = optionsRegex.search(optiontextTags[j].get_text())
        kprimQuestions[i].options.append(mo.groups()[1])
    while len(kprimQuestions[i].options) < 4:
        kprimQuestions[i].options.append("")

# get answers
for i in range(len(kprimHtmlTags)):
    optionTags = kprimHtmlTags[i].select(".solution .ilc_qanswer_Answer")
    del optionTags[0]
    for j in range(len(optionTags)):
        if optionTags[j].find_all("img")[0]["title"] == "Ausgewählt":
            kprimQuestions[i].answers.append(True)
        elif optionTags[j].find_all("img")[1]["title"] == "Ausgewählt":
            kprimQuestions[i].answers.append(False)

# get quiz title and write sources
quizTitle = soup.select("#il_mhead_t_focus")[0].get_text()
sourcePrefix = "ILIAS, " + quizTitle
for question in kprimQuestions:
    question.sources = sourcePrefix + ", ID: " + str(question.id)

# get extra text
feedbackRegex = re.compile(r"ilc_qfeed(w|r)_Feedback(Wrong|Right)")
for i in range(len(kprimHtmlTags)):
    feedbackTag = kprimHtmlTags[i].find(class_=feedbackRegex)
    if feedbackTag:
        kprimQuestions[i].extra1 = feedbackTag.get_text().strip()

# create CSV text
logging.debug("Creating CSV text for Kprim questions...")
newlineRegex = re.compile(r"(\r|\n)")
doublequoteRegex = re.compile(r'"')
kprimCSV = ""
for question in kprimQuestions:
    kprimCSV += '"' + question.title + '"'
    qtextstring = newlineRegex.sub("<br />", question.qtext)
    qtextstring = doublequoteRegex.sub('""', qtextstring)
    kprimCSV += ',"' + newlineRegex.sub("<br />", question.qtext) + '"'
    for option in question.options:
        optstring = newlineRegex.sub("<br />", option)
        optstring = doublequoteRegex.sub('""', optstring)
        kprimCSV += ',"' + optstring + '"'
    ansstring = ""
    for answer in question.answers:
        if answer:
            ansstring += "1 "
        else:
            ansstring += "0 "
    kprimCSV += ',"' + ansstring.strip() + '"'
    srcstring = newlineRegex.sub("<br />", question.sources)
    srcstring = doublequoteRegex.sub('""', srcstring)
    kprimCSV += ',"' + srcstring + '"'
    extrastring = newlineRegex.sub("<br />", question.extra1)
    extrastring = doublequoteRegex.sub('""', extrastring)
    kprimCSV += ',"' + extrastring + '"'
    tagstring = newlineRegex.sub("<br />", args.tags.strip())
    tagstring = doublequoteRegex.sub('""', tagstring)
    kprimCSV += ',"' + tagstring + '"\n'
kprimCSV = kprimCSV.strip()
logging.debug("CSV text for Kprim questions is " + str(len(kprimCSV)) + \
    " chars long.")

# write the file
kprimFileName = args.resultFile.strip(".html") + "_Kprim.csv"
logging.debug("Writing Kprim questions to " + kprimFileName)
f = open(kprimFileName, "w")
f.write(kprimCSV)
f.close()
logging.info("Wrote Kprim questions from " + args.resultFile + " to " + \
    kprimFileName)
print("Wrote " + str(len(kprimQuestions)) + " Kprim questions from " + \
    args.resultFile + " to " + kprimFileName)

# find A type multiple choice questions
mcAHtmlTags = soup.select(".solution .ilc_question_SingleChoice")
for i in range(len(mcAHtmlTags)):
     for parent in mcAHtmlTags[i].parents:
        if parent.get("class") and "pdfContent" in parent.get("class"):
            mcAHtmlTags[i] = parent
logging.debug("Found " + str(len(mcAHtmlTags)) + " A type questions.")

# get question ids and create mcA objects
idRegex = re.compile(r"\[ID: (\d+)\]")
aQuestions = []
for i in range(len(mcAHtmlTags)):
    titleTag = mcAHtmlTags[i].find(class_="questionTitle")
    mo = idRegex.search(titleTag.get_text())
    id = int(mo.groups()[0])
    aQuestions.append(mcA(id))

# get question titles
titleRegex = re.compile(r"^\d+\. +((.*)\w) +\[")
for i in range(len(mcAHtmlTags)):
    titleTag = mcAHtmlTags[i].find(class_="questionTitle")
    mo = titleRegex.search(titleTag.get_text())
    aQuestions[i].title = mo.groups()[0]

# get question text
for i in range(len(mcAHtmlTags)):
    questionTag = mcAHtmlTags[i].find(class_="ilc_qtitle_Title")
    qtext = questionTag.get_text()
    aQuestions[i].qtext = qtext.strip()

# get answer options
optionsRegex = re.compile(r"(\n|\t)*(.*)(\n|\t)*")
for i in range(len(mcAHtmlTags)):
    optiontextTags = mcAHtmlTags[i].select(".solution .answertext")
    for j in range(len(optiontextTags)):
        mo = optionsRegex.search(optiontextTags[j].get_text())
        aQuestions[i].options.append(mo.groups()[1])
    while len(aQuestions[i].options) < 5:
        aQuestions[i].options.append("")

# get answers
for i in range(len(mcAHtmlTags)):
    optionTags = mcAHtmlTags[i].select(".solution .ilc_qanswer_Answer")
    for j in range(len(optionTags)):
        if optionTags[j].find("img")["title"] == "Ausgewählt":
            aQuestions[i].answers.append(True)
        elif optionTags[j].find("img")["title"] == "Nicht ausgewählt":
            aQuestions[i].answers.append(False)

# get quiz title and write sources
quizTitle = soup.select("#il_mhead_t_focus")[0].get_text()
sourcePrefix = "ILIAS, " + quizTitle
for question in aQuestions:
    question.sources = sourcePrefix + ", ID: " + str(question.id)

# get extra text
feedbackRegex = re.compile(r"ilc_qfeed(w|r)_Feedback(Wrong|Right)")
for i in range(len(mcAHtmlTags)):
    feedbackTag = mcAHtmlTags[i].find(class_=feedbackRegex)
    if feedbackTag:
        aQuestions[i].extra1 = feedbackTag.get_text().strip()

# create CSV text
logging.debug("Creating CSV text for A questions...")
newlineRegex = re.compile(r"(\r|\n)")
doublequoteRegex = re.compile(r'"')
aCSV = ""
for question in aQuestions:
    aCSV += '"' + question.title + '"'
    qtextstring = newlineRegex.sub("<br />", question.qtext)
    qtextstring = doublequoteRegex.sub('""', qtextstring)
    aCSV += ',"' + newlineRegex.sub("<br />", question.qtext) + '"'
    for option in question.options:
        optstring = newlineRegex.sub("<br />", option)
        optstring = doublequoteRegex.sub('""', optstring)
        aCSV += ',"' + optstring + '"'
    ansstring = ""
    for answer in question.answers:
        if answer:
            ansstring += "1 "
        else:
            ansstring += "0 "
    aCSV += ',"' + ansstring.strip() + '"'
    srcstring = newlineRegex.sub("<br />", question.sources)
    srcstring = doublequoteRegex.sub('""', srcstring)
    aCSV += ',"' + srcstring + '"'
    extrastring = newlineRegex.sub("<br />", question.extra1)
    extrastring = doublequoteRegex.sub('""', extrastring)
    aCSV += ',"' + extrastring + '"'
    tagstring = newlineRegex.sub("<br />", args.tags.strip())
    tagstring = doublequoteRegex.sub('""', tagstring)
    aCSV += ',"' + tagstring + '"\n'
aCSV = aCSV.strip()
logging.debug("CSV text for A questions is " + str(len(aCSV)) + \
    " chars long.")

# write the file
aFileName = args.resultFile.strip(".html") + "_A.csv"
logging.debug("Writing A questions to " + aFileName)
f = open(aFileName, "w")
f.write(aCSV)
f.close()
logging.info("Wrote A questions from " + args.resultFile + " to " + \
    aFileName)
print("Wrote " + str(len(aQuestions)) + " A questions from " + \
    args.resultFile + " to " + aFileName)
