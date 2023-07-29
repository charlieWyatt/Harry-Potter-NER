from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging
import re
import json

#import Predictorpredictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/coref-model-2018.02.05.tar.gz")



# reading in harry potter
with open("harrypotter1.txt", "r", encoding="utf-8") as file:
    contents = file.read()


contents = re.sub(r'Page \| \d+ Harry Potter and the Philosophers Stone - J.K. Rowling', '', contents)
contents = re.sub(r'Harry Potter and the Philosophers Stone - J.K. Rowling', '', contents)

chapters = []

chapters.append(contents.split('THE VANASHIG GLASS ')[0]) # before chapter 2 starts
chapters.append(contents.split('THE VANASHIG GLASS ')[1].split('THE LETTERS FROM NO ONE ')[0]) # between chapter 2 and 3
chapters.append(contents.split('THE LETTERS FROM NO ONE ')[1].split('THE KEEPER OF THE KEYS ')[0]) # between chapter 3 and 4
chapters.append(contents.split('THE KEEPER OF THE KEYS ')[1].split('DIAGON ALLY ')[0]) # between chapter 4 and 5
chapters.append(contents.split('DIAGON ALLY ')[1].split('THE JOURNEY FROM PLATFORM \nNINE AND THREE-QUARTERS ')[0]) # between chapter 5 and 6
chapters.append(contents.split('THE JOURNEY FROM PLATFORM \nNINE AND THREE-QUARTERS ')[1].split('THE SORTING HAT ')[0]) # between chapter 6 and 7
chapters.append(contents.split('THE SORTING HAT ')[1].split('THE POTIONS MASTER ')[0]) # between chapter 7 and 8
chapters.append(contents.split('THE POTIONS MASTER ')[1].split('THE MIDNIGHT DUEL ')[0]) # between chapter 8 and 9
chapters.append(contents.split('THE MIDNIGHT DUEL ')[1].split('HALLOWEEN ')[0]) # between chapter 9 and 10
chapters.append(contents.split('HALLOWEEN ')[1].split('QUIDDITCH ')[0]) # between chapter 10 and 11
chapters.append(contents.split('QUIDDITCH ')[1].split('THE MIRROR OF ERISED ')[0]) # between chapter 11 and 12
chapters.append(contents.split('THE MIRROR OF ERISED ')[1].split('NORBERT THE NORWEGIAN \nRIDGEBACK ')[0]) # between chapter 12 and 13
chapters.append(contents.split('NORBERT THE NORWEGIAN \nRIDGEBACK ')[1].split('THE FORBIDDEN FOREST ')[0]) # between chapter 13 and 14
chapters.append(contents.split('THE FORBIDDEN FOREST ')[1].split('THROUGH THE TRAPDOOR ')[0]) # between chapter 14 and 15
chapters.append(contents.split('THE MAN WITH TWO FACES')[1]) # Chapter 15

print("Finished splitting chapters")

## Ensuring there is only two splits for each chapter i.e. one chapter in the whole book
# print(len(contents.split('THE VANASHIG GLASS ')))
# print(len(contents.split('THE LETTERS FROM NO ONE ')))
# print(len(contents.split('THE KEEPER OF THE KEYS ')))
# print(len(contents.split('DIAGON ALLY ')))
# print(len(contents.split('THE JOURNEY FROM PLATFORM \nNINE AND THREE-QUARTERS ')))
# print(len(contents.split('THE SORTING HAT ')))
# print(len(contents.split('THE POTIONS MASTER ')))
# print(len(contents.split('THE MIDNIGHT DUEL ')))
# print(len(contents.split('HALLOWEEN ')))
# print(len(contents.split('QUIDDITCH ')))
# print(len(contents.split('THE MIRROR OF ERISED ')))
# print(len(contents.split('NORBERT THE NORWEGIAN \nRIDGEBACK ')))
# print(len(contents.split('THE FORBIDDEN FOREST ')))
# print(len(contents.split('THROUGH THE TRAPDOOR ')))
# print(len(contents.split('THE MAN WITH TWO FACES')))

# print(firstChapter[len(firstChapter)-1000:])



# firstChapter = re.sub(r'\n', '', firstChapter)
# sentences = firstChapter.split('.')

# firstTenSentences = ""
# print(len(sentences))

# i=0
# for sentence in sentences:
#   if i == 10:
#     break
#   firstTenSentences += sentence +'.'
#   i +=1

# print(firstTenSentences)


pronouns = [
    "I", "You", "He", "She", "It", "We", "They",
    "Me", "You", "Him", "Her", "Us", "Them",
    "Myself", "Yourself", "Himself", "Herself", "Itself", "Ourselves", "Themselves",
    "My", "Your", "His", "Her", "Its", "Our", "Their",
    "Mine", "Yours", "His", "Hers", "Ours", "Theirs",
    "This", "That", "These", "Those",
    "Who", "Whom", "Whose",
    "Which", "What", "Whatever",
    "Somebody", "Someone", "Something",
    "Anybody", "Anyone", "Anything",
    "Everybody", "Everyone", "Everything",
    "Nobody", "No one", "Nothing",
    "All", "Both", "Few", "Many", "None", "Several", "Some"
]

predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz")
# print(predictor.predict(
#     document="Paul Allen was born on January 21, 1953, in Seattle, Washington, to Kenneth Sam Allen and Edna Faye Allen. Allen attended Lakeside School, a private school in Seattle, where he befriended Bill Gates, two years younger, with whom he shared an enthusiasm for computers."
# ))

def entity_recognition(text, predictor_model):

    sent = text
    pred = predictor_model.predict(    
            document= sent
    )


    # loop through with this. Then get the most frequent used word of the cluster. then assign each occuerence of the cluster to the most frequent name
    clusters = pred['clusters']
    document = pred['document'] 
    n = 0
    doc = {}
    for obj in document:    
        doc.update({n :  obj}) #what I'm doing here is creating a dictionary of each word with its respective index, making it easier later.    
        n = n+1

    clus_all = []
    cluster = []
    clus_one = {}
    for i in range(0, len(clusters)):    
        one_cl = clusters[i]    
        for count in range(0, len(one_cl)):           
            obj = one_cl[count]        
            for num in range((obj[0]), (obj[1]+1)):            
                for n in doc:                
                    if num == n:                 
                        cluster.append(doc[n]) 
        clus_all.append(cluster)       
        cluster = []     
    print(clus_all) #And finally, this shows all coreferences



    clusters_info = []
    # summarising what each cluster is about
    for cluster in clusters:
        cluster_info = {}
        # find the longest part of the cluster (probably the most informative if it is a group title)
        longest = max([sublist[1] - sublist[0] for sublist in cluster])
        for ranges in cluster:
            range_length = ranges[1] - ranges[0]
            if range_length == longest:
                cluster_info['longest'] = " ".join(document[ranges[0]:ranges[1]+1])
        # print(longest)

        # find the most repeated part of the cluster (probably the most recognisable if it is a single individual)
        freq = {}
        for ranges in cluster:
            for el in range(ranges[0], ranges[1]+1):
                word = document[el]
                #print(word)
                try:
                    freq[document[el]] += 1
                except:
                    freq[word] = 1
                    if word[0].isupper() and word not in pronouns:
                        try:
                            cluster_info['proper_nouns'].append(word)
                        except:
                            cluster_info['proper_nouns'] = [word]
        cluster_info['most_common'] = max(freq)
        cluster_info['total_refs'] = len(cluster)
        clusters_info.append(cluster_info)


    return(clusters_info, clusters, pred['document'])

i = 1
for chapter in chapters:
    print("Starting chapter " + str(i))
    clusters_info, clusters, document = entity_recognition(chapter, predictor)
    # Write the list to a JSON file
    with open("output_info_chapter" + str(i) + ".json", "w") as file:
        json.dump(clusters_info, file)

    # Write the list to a JSON file
    with open("output_cluster_chapter" + str(i) + ".json", "w") as file:
        json.dump(clusters, file)

    # Write the list to a JSON file
    with open("output_raw_chapter" + str(i) + ".json", "w") as file:
        json.dump(document, file)

    print("Finished chatper " + str(i))
    i += 1

print("Finished all chapters")