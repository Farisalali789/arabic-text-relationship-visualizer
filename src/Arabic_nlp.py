import stanza
from rdflib import Graph, URIRef, Namespace    # Resource Description Framework (RDF)
from pyvis.network import Network
from urllib.parse import quote, unquote



"""with open("story_3.txt", 'r', encoding="utf-8") as file:
    _text = file.read()"""

# Stanza Library
stanza.download('ar')

nlp = stanza.Pipeline('ar', processors='tokenize,pos,lemma,depparse', use_gpu=True, logging_level= "FATAL")


text = "تعيش الذئاب في الصحراء العربية حيث تصطاد الأرانب البرية في الليل. تراقب البومة الصحراوية هذه المطاردات من مواقعها العالية، وغالباً ما تستفيد من بقايا فرائس الذئاب. في فصل الصيف، يهاجم النسر الذهبي صغار الذئاب عندما تبتعد عن مجموعتها، بينما تحمي الذئاب البالغة صغارها بشراسة. تتجنب الثعالب الصحراوية مناطق الذئاب، لكنها تشارك البوم في البحث عن القوارض الصغيرة."

#text = "تعيش الذئاب في الصحراء العربية حيث تصطاد الأرانب البرية في الليل."

text = nlp(text)


print(len(text.sentences))

def get_word(nlp_text, id):
    for sentence in nlp_text.sentences:
        for word in sentence.words:
            if word.id == id:
                return word
    return None


for x in text.sentences:
    for y in x.words:
        print(y)

triples = []

for sentence in text.sentences:
    subject = ""
    verb = ""
    object = ""
    for word in sentence.words:     #    The golden eagle eats the fox and then the bird he returns to the nest
        if word.upos == "VERB":
            verb = word
            for rel_word in sentence.words:
                if rel_word.head == verb.id and rel_word.deprel == "nsubj" and rel_word.upos != "PRON":
                    second_word = get_word(text, rel_word.id + 1)
                    if second_word.head == rel_word.id:
                        if second_word.deprel == "amod" or second_word.deprel == "nmod":
                            subject = f"{rel_word.text} {second_word.text}"
                        else:
                            subject = rel_word.text
                    else:
                        subject = rel_word.text
                elif rel_word.head == verb.id:
                    if rel_word.deprel == "obj":
                       second_word = get_word(text, rel_word.id + 1)
                       if second_word.head == rel_word.id:
                           if second_word.deprel == "amod" or second_word.deprel == "nmod":
                              object = f"{rel_word.text} {second_word.text}"
                           else:
                               object = rel_word.text
                       else:
                           object = rel_word.text
                if subject and verb and object:
                    temp_list = [subject, verb.text, object]
                    triples.append(temp_list)
                    object = ""


rdf_graph = Graph()

SPACE = Namespace("http://example.org/")

print("RDF Triples in the Graph:")
for triple in triples:
    rdf_graph.add((SPACE[quote(triple[0])],SPACE[quote(triple[1])],SPACE[quote(triple[2])]))
    print(f"Subject => {triple[0]} Verb => {triple[1]} Object => {triple[2]}")

rdf_graph.serialize("entity_relations.rdf", format="turtle")
print("\nRDF data has been saved to 'entity_relation.rdf'")

net = Network(notebook=True, width="100%", height="600px", bgcolor="#ffffff", font_color="black")

# Add nodes and edges based on RDF triples

nodes_set = ()

for subject, verb, object in rdf_graph:

    subject_name = unquote(subject.split('/')[-1])
    predicate_name = unquote(verb.split('/')[-1])
    object_name = unquote(object.split('/')[-1])

    net.add_node(subject_name, title=subject_name)
    net.add_node(object_name, title=object_name)
    net.add_edge(subject_name, object_name, label=predicate_name)

net.show("Entity_relation_web.html")











