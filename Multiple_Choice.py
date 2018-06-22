import copy
import time
from anki.collection import _Collection
from anki.utils import splitFields
from aqt.utils import showInfo
import re
import random
    
oldRenderQA = _Collection._renderQA
def _renderQA(self,data,qfmt=None,afmt=None):
    origFieldMap = self.models.fieldMap
    model = self.models.get(data[2])
    if data[0] is None:
        card = None
    elif data[0] == 1:
        card = None
    else:
        try:
            card = self.getCard(data[0])
        except:
            card = None
    flist = splitFields(data[6])
    mc_fields = []
    mc_answer = ''
    
    for (name, (idx, conf)) in self.models.fieldMap(model).items():
        if re.match('^MC_[0-9]+', name):
            if flist[idx] != '':
                mc_fields.append(flist[idx])
        if name == u'MC_{0}'.format(mc_answer):
            mc_answer = flist[idx]
        if name == u'MC_Ans':
            mc_answer = flist[idx]
    def tmpFieldMap(m):
        "Mapping of field name -> (ord, field)."
        d = dict((f['name'], (f['ord'], f)) for f in m['flds'])
        newFields = [u'MC_Questions', u'MC_Answer']
        for i,f in enumerate(newFields):
            d[f] = (len(m['flds'])+i,0)
        return d
    self.models.fieldMap = tmpFieldMap
    origdata = copy.copy(data)
    data[6] += "\x1f"
    random.shuffle(mc_fields)
    answer_index = -1
    for i, answer in enumerate(mc_fields):
        if answer == mc_answer:
            answer_index = i
            break
    mc_fields = [u'({0}) {1}'.format(i+1, val) for i, val in enumerate(mc_fields)]
    data[6] += u'<br>'.join(mc_fields)
    data[6] += "\x1f"
    if answer_index != -1 and len(mc_fields) > answer_index:
        mc_fields[answer_index] = u'<span style="color: blue;">{0}</span>'.format(mc_fields[answer_index])
    data[6] += '<br>'.join(mc_fields)
    result = oldRenderQA(self,data,qfmt,afmt)
    data = origdata
    self.models.fieldMap = origFieldMap
    return result
    
def previewCards(self, note, type=0):
    existingTemplates = {c.template()[u'name'] : c for c in note.cards()}
    if type == 0:
        cms = self.findTemplates(note)
    elif type == 1:
        cms = [c.template().name() for c in note.cards()]
    else:
        cms = note.model()['tmpls']
    if not cms:
        return []
    cards = []
    for template in cms:
        if template[u'name'] in existingTemplates:
            card = existingTemplates[template[u'name']]
        else:
            card = self._newCard(note, template, 1, flush=False)
        cards.append(card)
    return cards
    
_Collection._renderQA = _renderQA
_Collection.previewCards = previewCards
