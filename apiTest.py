# -*- coding: utf-8 -*-

from watson_developer_cloud import NaturalLanguageClassifierV1
from watson_developer_cloud import ToneAnalyzerV3




def apiNLCTest(comment_text):
    api_key="LiI3o53WHaOU02ATKIwKhSQdirvntK1lZUPA6rhdEwCZ"
    workspace_ID="6deb62x509-nlc-477"


    natural_language_classifier = NaturalLanguageClassifierV1(iam_apikey=api_key)
    #classifier instance 
    response = natural_language_classifier.classify(workspace_ID, comment_text)
    result=[]
    response_new = response.result
#    return(response_new)
    if "classes" in response_new.keys():
        for predicted_class in response_new["classes"]:
            result.append([predicted_class['class_name'],predicted_class['confidence']])
        return(result)
    
def apiToneTest(comment_text):

    tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='MODwXhl7pCy1NQonErss_VNVgUmXELmQmKKV02HhxW1u',
    url='https://gateway.watsonplatform.net/tone-analyzer/api')

#    comment_text = "Yo bitch Ja Rule is more succesful then you'll ever be whats up with you and hating you sad mofuckas...i should bitch slap ur pethedic white faces and get you to kiss my ass you guys sicken me. Ja rule is about pride in da music man. dont diss that shit on him. and nothin is wrong bein like tupac he was a brother too...fuckin white boys get things right next time."

    tone_analysis = tone_analyzer.tone(
        {'text': comment_text},
        'application/json'
    ).get_result()
#    print(tone_analysis)
    if(len(tone_analysis["document_tone"]["tones"])==0) :
        return ["","No Tone"]
    else:
        return(tone_analysis["document_tone"]["tones"][0]["score"],tone_analysis["document_tone"]["tones"][0]["tone_name"])
