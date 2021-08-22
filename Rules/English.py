#!/usr/bin/env python3
# Copyright (c) 2006 Bermi Ferrer Martinez
# info at bermi dot org
# See the end of this file for the free software, open source license (BSD-style).

import re
#from Base import Base

#class English (Base):
class English(object):
    """
    Inflector for pluralize and singularize English nouns.
    
    This is the default Inflector for the Inflector obj
    """
    
    irregular_words = {
        'person' : 'people',
        'man' : 'men',
        'child' : 'children',
        'sex' : 'sexes',
        'foot' : 'feet',
        'goose' : 'geese',
        'tooth' : 'teeth',
    }

    reserve_words = {
        'ox' : 'oxen',
        'genus': 'genera',
        'corpus': 'corpora',
        'concerto': 'concerti',
        'bus' : 'buses',
        'virus' : 'viruses',
        'apparatus': 'apparatuses',
        'die' : 'dice',
        'this' : 'these',
        'that' : 'those',
        'quiz' : 'quizzes',
        'polka' : 'polkas',
        'passerby' : 'passersby',
        'sarcoma' : 'sarcomata', 
        'schema' : 'schemata', 
        'stigma' : 'stigmata', 
        'stoma' : 'stomata', 
        'cherub' : 'cherubim',
        'kibbutz' : 'kibbutzim',
        'seraph' : 'seraphim',
        'mum' : 'mums',
        'boa' : 'boe',
    }
        
    uncountable_words = ['aircraft','equipment', 'information', 'rice', \
        'money', 'species', 'series', 'fish', 'sheep', 'shrimp', 'sms', \
        'moose', 'bison', 'deer', 'means', 'scissors', 'species', 'swine', \
        'salmon','scum','sorghum',
        'meerschuam',
        'offspring',
        'phoenix',
        'talcum',
        'vespers',
        'wampum',
        ]
        
    inflector_rules = [
        ['(.*)',                        'eau',          'eaux'],
        ['(.*)',                        'menon',        'mena'],
        ['(.*)',                        'terion',       'teria'],
        ['((.*)m|[^b]l)',               'ouse',         'ice'],
        ['((.*)[dlr])',                 'ix',           'ices'],
        ['((.*)[dpt])',                 'ex',           'ices'],
        ['((.*)ar|f|oo)',               'f',            'fs'],
        ['(.*)',                        '[f|fe]',       'ves'],
#        ['((.*)pian|sol|temp)',         'o',            'os'],
        ['((.*)[aeioulnp])',            'o' ,           'os'],
        ['((.*)[o|x|z|ch|ss|sh])',      '',             'es'],
        ['(.*)',                        '-in-law' ,     's-in-law'],
        ['(.*)',                        'ful',          'sful'],
        ['(.*)',                        'is',           'es'],
        ['((.*)d|[aeiouy]n|p|pl|r|s|t)','us',           'uses'],
        ['((.*)bu)',                    's',            'ses'],
        ['(.*)',                        'us',           'i'],
        ['((.*)a|b|dumd|e|g|h|k|(d|l|p|s|sy)l|o|r|s)',  'um',   'ums'],
        ['(.*)',                        'um',           'a'],
        ['(.*[aeiou])'                  'a',            'as'],
        ['(.*)',                        'a' ,           'ae'],
        ['((.*)[^aeiouy]|qu)',          'y',            'ies'],
        ['(.*)',                        's',            'ses'],
        ['(.*)',                        '',             's']
    ]
    to_plural_compiled= [re.compile('(?i)'+r[0]+r[1]+'$') for r in inflector_rules]

    def pluralize(self, word) :
        '''Pluralizes English nouns.'''
        
        #get rules from 
        #http://web2.uvcs.uvic.ca/elc/studyzone/330/grammar/irrplu.htm
        #http://www2.gsu.edu/~wwwesl/egw/pluralsn.htm
        
        lower_cased_word = word.lower();

        for uncountable_word in self.uncountable_words:
            if lower_cased_word[-1*len(uncountable_word):] == uncountable_word :
                return word
        
        for res_word in self.reserve_words.keys():
            if res_word == word:
                return self.reserve_words[res_word]
        
        for irregular in self.irregular_words.keys():
            match = re.search('('+irregular+')$',word, re.IGNORECASE)
            if match:
                return re.sub('(?i)'+irregular+'$', match.expand('\\1')[0]\
                    +self.irregular_words[irregular][1:], word)

        r = self.to_plural_compiled
        for idx in range(len(r)):
            if r[idx].match(word):
                return r[idx].sub('\\1'+self.inflector_rules[idx][2], word)
        
        return word


    def singularize (self, word) :
        '''Singularizes English nouns.'''
        
        rules = [
            ['(?i)eaux$' , 'eau'],
            ['(?i)mena$' , 'menon'],
            ['(?i)teria$' , 'terion'],
            ['(?i)([m|l])ice$' , '\\1ouse'],
            ['(?i)ices$' , '|ix|ex'],
            ['(?i)ves$' , '|f|fe'],
            ['(?i)os$' , 'o'],
            ['(?i)(o|x|z|ch|ss|sh)es$' , '\\1'],
            ['(?i)s-in-law$' , '-in-law'],
            ['(?i)sful$' , 'ful'],
            ['(?i)(d|(a|e|i|o|u)n|p|pl|r|s|t)uses$' , '\\1us'],
            ['(?i)(a|b|dumd|e|g|h|k|(d|l|p|s|sy)l|o|r|s)ums$' , '\\1um'],
            ['(?i)a$' , 'um'],
            ['(?i)i$' , 'us'],
            ['(?i)ses$' , 's'],
            ['(?i)es$' , 'is'],
            ['(?i)(a|e|i|o|u)as$' , '\\1a'],
            ['(?i)ae$' , 'a'],
            ['(?i)ies$' , 'y'],
            ['(?i)s$' , '']
        ]
    
        irregular_words = dict(
            [[self.irregular_words[i],i] for i in self.irregular_words.keys()] )
    
        reserve_words = dict(
            [[self.reserve_words[i],i] for i in self.reserve_words.keys()] )

        lower_cased_word = word.lower();
    
        for uncountable_word in self.uncountable_words:
            if lower_cased_word[-1*len(uncountable_word):] == uncountable_word :
                return word
            
        for irregular in irregular_words.keys():
            match = re.search('('+irregular+')$',word, re.IGNORECASE)
            if match:
                return re.sub('(?i)'+irregular+'$', match.expand('\\1')[0]+irregular_words[irregular][1:], word)
            
        for res_word in self.reserve_words.keys():
            if res_word == word:
                return self.reserve_words[res_word]

        for rule in range(len(rules)):
            match = re.search(rules[rule][0], word, re.IGNORECASE)
            if match :
                groups = match.groups()
                for k in range(0,len(groups)) :
                    if groups[k] == None :
                        rules[rule][1] = rules[rule][1].replace('\\'+str(k+1), '')
                        
                return re.sub(rules[rule][0], rules[rule][1], word)
        
        return word
    
    tense_skel_aux = [
        #be
        ['',                'be',   'was',  'been', 'is',   'being'],
        ['',                'is',   'was',  'been', 'is',   'being'],
        ['',                'am',   'was',  'been', 'am',   'being'],
        ['',                'are',  'were', 'been', 'are',  'being'],
        ['',                'has',  'had',  'had',  'has',  'having'],
        ['',                'have', 'had',  'had',  'has',  'having'],
        ['',                'will', 'would','would','',  ''],
        ['',                'shall','should','should','',  ''],
    ]

    tense_skel_1 = [
        #present, past, perfect, singular, continuous
        #all
        ['(?i)(f)',         'all',  'ell',  'allen','alls', 'alling'],
        #ake
        ['(?i)([hst])',     'ake',  'ook',  'aken', 'akes', 'aking'],
        ['(?i)(w)',         'ake',  'oke',  'oken', 'akes', 'aking'],
        ['(?i)(m)',         'ake',  'ade',  'ade',  'akes', 'aking'],
        #and
        ['(?i)(st)',        'and',  'ood',  'ood',  'ands', 'anding'],
        #ang
        ['(?i)(h)',         'ang',  'ung',  'ung',  'angs', 'anging'],
        #ast
        ['(?i)(c)',         'ast',  'ast',  'ast',  'asts', 'asting'],
        #atch
        ['(?i)(c)',         'atch', 'aught','aught','atchs','atching'],
        #ave
        ['(^h|(?i)(beh))',  'ave',  'ad',   'ad',   'as',   'aving'],
        #aw
        ['(?i)(dr)',        'aw',   'ew',   'awn',  'aws',  'awing'],
        ['(?i)(bl)',        'aw',   'awd',  'awn',  'aws',  'awing'],
        #ay
        ['(?i)(sl)',        'ay',   'ew',   'ain',  'ays',  'aying'],
        ['(?i)(pl)',        'ay',   'ayed', 'ayed', 'ays',  'aying'],
        ['(^l|(^over|^out|^under)l|(?i)(p|s))','ay','aid','aid','ays','aying'],
        #each
        ['(?i)(t)',         'each', 'aught','aught','eachs','eaching'],
        #ead
        ['(?i)(tr)',        'ead',  'od',   'odden','eads', 'eading'],
        ['(?i)(l)',         'ead',  'ed',   'ed',   'eads', 'eading'],
        ['(?i)(fr|r|spr)',  'ead',  'ead',  'ead', 'eads', 'eading'],
        #eak
        ['(?i)(br|sp)',     'eak',  'oke',  'oken','eaks', 'eaking'],
        #eal
        ['(?i)(d)',         'eal',  'ealt', 'ealt','eals', 'ealing'],
        ['(?i)(st)',        'eal',  'ole',  'olen','eals', 'ealing'],
        #eam
        ['(?i)(dr)',        'eam',  'eamt', 'eamt','eams', 'eaming'],
        #ean
        ['(?i)(l|m)',       'ean',  'eant', 'eant','eans', 'eaning'],
        #earn
        ['(?i)([l])',         'earn', 'earn', 'earn', 'earns','earning'],
        #ear
        ['(?i)(b|sh|t|w)',  'ear',  'ore',  'orn', 'ears', 'earing'],
        ['(?i)(h)',         'ear',  'eard', 'eard' 'ears', 'earing'],
        #eat
        ['(?i)(sw)',        'eat',  'eat',  'eat', 'eats','eating'],
        ['(?i)(b)',         'eat',  'eat',  'eaten','eats','eating'],
        ['(^over|^under|^)','eat',  'ate',  'eaten','eats','eating'],
        #eave
        ['(?i)([ber|l])',   'eave', 'eft',  'eft', 'eaves','eaving'],
        ['(?i)([rw])',      'eave', 'ove',  'oven','eaves','eaving'],
        #ee
        ['(?i)(s)',         'ee',   'aw',   'een', 'ees', 'eeing'],
        ['(?i)(l)',         'ee',   'ed',   'ed' , 'ees', 'eeing'],
        #eech
        ['(?i)(s)',         'eech', 'ought','ought','eechs','eeching'],
        #eed
        ['(?i)([^n])',      'eed',  'ed',   'ed',  'eeds','eeding'],
        #eek
        ['(?i)(s)',         'eek',  'ought','ought','eeks','eeking'],
        #eel
        ['(?i)(f|kn)',      'eel',  'elt',  'elt',  'eels','eeling'],
        #eep
        ['(?i)(cr|k|sl|w)', 'eep',  'ept',  'ept', 'eeps','eeping'],
        #eet
        ['(?i)(m)',         'eet',  'et',   'et',  'eets','eeting'],
        #eeve
        ['(?i)(r)',         'eeve', 'ove',  'ove', 'eeves','eeving'],
        #eeze
        ['(?i)(r)',         'eeze', 'oze',  'ozen','eezes','eezing'],
        #ell
        ['(?i)(s|t)',       'ell',  'old',  'old', 'ells','elling'],
        ['(?i)(dw|sp)',     'ell',  'elt',  'elt', 'ells','elling'],
        ['(?i)(sw)',        'ell',  'elled','ollen','ells','elling'],
        #elt
        ['(?i)(m)',         'elt',  'elted','olten','elts','elting'],
        #end
        ['(?i)([bhlprs])',  'end',  'ent',  'ent', 'ends','ending'],
        #et
        ['(?i)(g)',         'et',   'ot',   'otten','ets', 'etting'],
        ['(?i)([blsw])',    'et',   'et',   'et',  'ets', 'etting'],
        #ew
        ['(?i)(h|r|s)',     'ew',   'ewed', 'ewn', 'ews', 'ewing'],
        #ex
        ['(?i)(v)',         'ex',   'ext',  'ext', 'exes','exing'],
        #go
        ['(?i)()',          'go',   'went', 'gone','goes','going'],
        #ick
        ['(?i)(st)',        'ick',  'uck',  'uck', 'icks','icking'],
        #id
        ['(?i)(forb)',      'id',   'ade',  'idden','ids','idding'],
        ['(?i)(b)',         'id',   'id',   'id',   'ids','idding'],
        #ie
        ['(?i)(l)',         'ie',   'ay',   'ane',  'ies','ying'],
        #ide
        ['(?i)(bet)',       'ide',  'ide',  'ide',  'ides','iding'],
        ['(?i)(.*[br])',    'ide',  'ode',  'idden','ides','iding'],
        ['(?i)(l)',         'ide',  'id',   'id',  'ides', 'iding'],
        ['(?i)(h)',         'ide',  'id',   'idden',  'ides', 'iding'],
        #ig
        ['(?i)(d)',         'ig',   'ug',   'ug',   'igs','igging'],
        #ight
        ['(?i)(f)',         'ight', 'ought','ought','ights', 'ighting'],
        ['(?i)(l)',         'ight', 'it',   'it', 'ights', 'ighting'],
        #ike
        ['(?i)(str)',       'ike',  'uck',  'uck', 'ikes','iking'],
        #ill
        ['(?i)(sp)',        'ill',  'ilt',  'ilt', 'ills','illing'],
        #im
        ['(?i)(sw)',        'im',   'am',   'um',  'ims', 'imming'],
        #in
        ['(?i)(beg|sp)',    'in',   'an',   'un',  'ins', 'inning'],
        ['(?i)(w)',         'in',   'on',   'on',  'ins', 'inning'],
        ['(?i)(g)',         'in',   'an',   'an',  'ins', 'inning'],
        #ind
        ['(?i)([bfrw])',    'ind',  'ound', 'ound','inds','inding'],
        #ine
        ['(?i)(sh)',        'ine',  'one',  'one', 'ines','ining'],
        ['(?i)(t)',         'ine',  'int',  'int', 'ines','ining'],
        #ing 
        ['(^r|^s|^spr)',    'ing',  'ang',  'ung', 'ings','inging'],
        ['(?i)(br|^p)',     'ing',  'ought','ought','ings','inging'],
        ['(?i)([^aeiouy](l|r|t|w))','ing','ung','ung','ings','inging'],
        #ink
        ['(?i)(r|s|t)',     'ink',  'ank',  'unk', 'inks','inking'],
        ['(?i)(l)',         'ink',  'unk',  'unk', 'inks','inking'],
        ['(?i)(th)',        'ink',  'ought','ought','inks','inking'],
        #ip
        ['(?i)(str)',       'ip',   'ipt',  'ipt', 'ips', 'ipping'],
        #ise
        ['(^ar|^r)',        'ise',  'ose',  'isen','ises','ising'],
        #it
        ['(?i)(f|h|kn|sl|spl)','it','it',   'it',  'its', 'itting'],
        ['(?i)(s|sp)',      'it',   'at',   'at',  'its', 'itting'],
        #ite
        ['(?i)(b)',         'ite',  'it',   'itten','ites','iting'],
        ['(?i)(sm|wr)',     'ite',  'ote',  'itten','ites','iting'],
        #ive
        ['(^r)',            'ive',  'ived', 'iven', 'ives','iving'],
        ['(?i)(r)',         'ive',  'ove',  'iven', 'ives','iving'],
        ['(?i)(g)',         'ive',  'ave',  'iven', 'ives','iving'],
        #o
        ['(?i)(d)',         'o',    'id',   'one',  'oes', 'oing'],
        #oe
        ['(^sh)',           'oe',   'ot',   'ot',   'oes', 'oeing'],
        #oil
        ['(^sp)',           'oil',  'oit',  'oit',  'oils','oiling'],
        #oist
        ['(h)',             'oist', 'oist', 'oist', 'oists','oisting'],
        #old
        ['(?i)(h)',         'old',  'eld',  'eld',  'olds','olding'],
        #ome
        ['(?i)(c)',         'ome',  'ame',  'ome',  'omes','oming'],
        #ont
        ['(?i)(w)',         'ont',  'ont',  'ont',  'onts','onting'],
        #oot
        ['(?i)(sh)',        'oot',  'ot',   'ot',   'oots','ooting'],
        #oose
        ['(?i)(ch)',        'oose', 'ose',  'osen', 'ooses','oosing'],
        #ose
        ['(?i)(l)',         'ose$', 'ost',  'ost',  'oses','osing'],
        #ost
        ['(?i)(c)',         'ost',  'ost',  'ost',  'oses','osing'],
        #ove
        ['(?i)(pr)',        'ove$', 'oved', 'oven', 'oves','oving'],
        #ow
        ['(?i)([^l]l|n|r)',   'ow',   'ew',   'own', 'ows', 'owing'],
        ['(?i)(.*[hms])',   'ow',   'owed', 'own', 'ows', 'owing'],
        #un
        ['(?i)(r)',         'un',   'an',   'un',  'uns', 'unning'],
        #urn
        ['(^b)',            'urn',  'urnt', 'urnt','urns','urning'],
        #urt
        ['(^h)',            'urt',  'urt',  'urt', 'urts','urting'],
        #ust
        ['(?i)(b|thr)',     'ust',  'ust',  'ust', 'usts','usting'],
        #uild
        ['(?i)(b)',         'uild', 'uilt', 'uilt','uilds','uilding'],
        #uit
        ['(?i)(q)',         'uit',  'uit',  'uit', 'uits', 'uiting'],
        #ut
        ['(?i)([chp])',     'ut',   'ut',   'ut',  'uts', 'utting'],
        #y
        ['(?i)([^aeiouy])', 'y',    'ied',  'ied',  'ies',  'ying'],
        #
    ]

    t_compiled_1 = []
    #for i in range(4):
    #    t_compiled_1.append( [ re.compile(ts[0]+ts[i+1]+'$') for ts in tense_skel_1 ] )
    t_compiled_1.append( [ re.compile(ts[0]+ts[1]+'$') for ts in tense_skel_1 ] )
    t_compiled_1.append( [ re.compile(ts[0]+ts[2]+'$') for ts in tense_skel_1 ] )
    t_compiled_1.append( [ re.compile(ts[0]+ts[3]+'$') for ts in tense_skel_1 ] )
    t_compiled_1.append( [ re.compile(ts[0]+ts[4]+'$') for ts in tense_skel_1 ] )


    tense_skel_122 = [
        ['(?i)(.*[^aeiouy][aeiouy])([^aeiouy])','','ed', 'ed','s','ing'],
    ]
    t_compiled_122 = []
    #for i in range(4):
    #    t_compiled_122.append( [ re.compile(ts[0]+ts[i+1]+'$') for ts in tense_skel_122 ] )
    t_compiled_122.append( [ re.compile(ts[0]+ts[1]+'$') for ts in tense_skel_122 ] )
    t_compiled_122.append( [ re.compile(ts[0]+ts[2]+'$') for ts in tense_skel_122 ] )
    t_compiled_122.append( [ re.compile(ts[0]+ts[3]+'$') for ts in tense_skel_122 ] )
    t_compiled_122.append( [ re.compile(ts[0]+ts[4]+'$') for ts in tense_skel_122 ] )


    tense_skel_122_reverse = [
        ['(?i)([^aeiouy][aeiouy])([^aeiouy]{2})','','ed', 'ed','s','ing'],
    ]
    t_compiled_122_reverse = []
    #for i in range(4):
    #    t_compiled_122_reverse.append( [ re.compile(ts[0]+ts[i+1]+'$') for ts in tense_skel_122_reverse ] )
    t_compiled_122_reverse.append( [ re.compile(ts[0]+ts[1]+'$') for ts in tense_skel_122_reverse ] )
    t_compiled_122_reverse.append( [ re.compile(ts[0]+ts[2]+'$') for ts in tense_skel_122_reverse ] )
    t_compiled_122_reverse.append( [ re.compile(ts[0]+ts[3]+'$') for ts in tense_skel_122_reverse ] )
    t_compiled_122_reverse.append( [ re.compile(ts[0]+ts[4]+'$') for ts in tense_skel_122_reverse ] )

    tense_skel_12 = [
        ['(?i)(str[aeiouy])([^aeiouy])','','ed', 'ed','s','ing'],
    ]

    tense_skel_normal = [
        ['(?i)',            'e',    'ed',   'ed',   'es',   'ing'],
        ['(?i)',            '',     'ed',   'ed',   's',    'ing'],
    ]


    def get_tense(self,word,_from,_to):
        """Get tense from word"""
        #1=present,2=past,3=perfect,4=singular,5=continuous

        #trap
        if _from != 1: _to = 1

        for rule in range(len(self.tense_skel_aux)):
            if word == self.tense_skel_aux[rule][_from]:
                return self.tense_skel_aux[rule][_to]

        for rule in range(len(self.t_compiled_1[_from-1])):
            if self.t_compiled_1[_from-1][rule].match(word):
                t = self.tense_skel_1
                reg = t[rule][0] + t[rule][_from] + '$'
                return re.sub(reg, '\\1'+t[rule][_to], word)

        if _from == 1:
            for rule in range(len(self.t_compiled_122[_from-1])):
                reg = self.t_compiled_122[rule][_from-1]
                if self.t_compiled_122[_from-1][rule].match(word):
                    t = self.tense_skel_122
                    #reg = t[rule][0] + t[rule][_from] + '$'
                    if _to == 4:
                        #return re.sub(reg, '\\1\\2'+t[rule][_to], word)
                        return reg.sub('\\1\\2'+t[rule][_to], word)
                    else:
                        #return re.sub(reg, '\\1\\2\\2'+t[rule][_to], word)
                        return reg.sub('\\1\\2\\2'+t[rule][_to], word)
        else:
            for rule in range(len(self.t_compiled_122_reverse[_from-1])):
                if self.t_compiled_122_reverse[_from-1][rule].match(word):
                    t = self.tense.skel_122_reverse
                    reg = t[rule][0] + t[rule][_from] + '$'
                    if _to == 4:
                        return re.sub(reg, '\\1\\2'+t[rule][_to], word)[:-1]
                    else:
                        return re.sub(reg, '\\1\\2'+t[rule][_to], word)[:-1]

        for rule in range(len(self.tense_skel_12)):
            reg = self.tense_skel_12[rule][0]+self.tense_skel_12[rule][_from]+'$'
            match = re.search(reg, word, re.IGNORECASE)
            if match :
                return re.sub(reg, '\\1\\2'+self.tense_skel_12[rule][_to], word)

        for rule in range(len(self.tense_skel_normal)):
            reg = self.tense_skel_normal[rule][0]+self.tense_skel_normal[rule][_from]+'$'
            match = re.search(reg, word, re.IGNORECASE)
            if match :
                return re.sub(reg, self.tense_skel_normal[rule][_to], word)

        return word

    def get_all(self,word):
        return [word, self.to_past(word), self.to_perfect(word), self.to_singular(word), self.to_continuous(word)]

    def to_past(self,word):
        return self.get_tense(word,1,2)

    def to_perfect(self,word):
        return self.get_tense(word,1,3)

    def to_singular(self,word):
        return self.get_tense(word,1,4)

    def to_continuous(self,word):
        return self.get_tense(word,1,5)

    def from_past(self,word):
        """Get present tense from past tense"""
        return self.get_tense(word,2,1)

    def from_perfect(self,word):
        """Get present tense from past perfect tense"""
        return self.get_tense(word,3,1)

    def from_singular(self,word):
        return self.get_tense(word,4,1)

    def from_continuous(self,word):
        return self.get_tense(word,5,1)

# Copyright (c) 2006 Bermi Ferrer Martinez
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software to deal in this software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of this software, and to permit
# persons to whom this software is furnished to do so, subject to the following
# condition:
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THIS SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THIS SOFTWARE.
