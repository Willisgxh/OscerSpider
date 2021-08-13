# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from neo4j import GraphDatabase
from py2neo import Graph, Node, Relationship, NodeMatcher

class OscerspiderPipeline:

    def __init__(self, uri, user, password):
        self.uri = uri
        self.user = user
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings.get('URI'),
            crawler.settings.get('NEO4J_USER'),
            crawler.settings.get('NEO4J_PASSWORD')
        )

    def open_spider(self, spider):
        self.client = Graph(self.uri, auth=(self.user, self.password))

    # def close_spider(self, spider):
    #     self.client.close()

    def process_item(self, item, spider):
        item_dict = dict(item)
        print(item_dict)

        matcher = NodeMatcher(self.client)
        if not matcher.match("Diseases", Diseases=item_dict.get('Diseases')):
            d = Node("Diseases", Diseases=item_dict.get('Diseases'))
            self.client.create(d)
        else:
            d = matcher.match("Diseases", Diseases=item_dict.get('Diseases'))[0]
        if not matcher.match("Symptoms", Symptoms=item_dict.get('Symptoms')):
            s = Node("Symptoms", Symptoms=item_dict.get('Symptoms'))
            self.client.create(s)
        else:
            s = matcher.match("Symptoms", Symptoms=item_dict.get('Symptoms'))[0]
        if not matcher.match("Causes", Causes=item_dict.get('Causes')):
            c = Node("Causes", Causes=item_dict.get('Causes'))
            self.client.create(c)
        else:
            c = matcher.match("Causes", Causes=item_dict.get('Causes'))[0]
        if not matcher.match("Diagnosis", Diagnosis=item_dict.get('Diagnosis')):
            dia = Node("Diagnosis", Diagnosis=item_dict.get('Diagnosis'))
            self.client.create(dia)
        else:
            dia = matcher.match("Causes", Causes=item_dict.get('Causes'))[0]
        if not matcher.match("Treatment", Treatment=item_dict.get('Treatment')):
            t = Node("Treatment", Treatment=item_dict.get('Treatment'))
            self.client.create(t)
        else:
            t = matcher.match("Treatment", Treatment=item_dict.get('Treatment'))[0]
        try:
            r1 = Relationship(d, "HAS", s)
            r2 = Relationship(d, "DUE_TO", c)
            r3 = Relationship(t, "TREAT", d)
            s = r1 | r2 | r3
            self.client.create(s)
        except UnboundLocalError:
            pass

            # session.run("MERGE (d: Dieases{Diseases: $diseases}) RETURN d", diseases=item_dict.get('Diseases'))
            # session.run("MERGE (s: Symptoms{Symptoms: $symptoms})", symptoms=item_dict.get('Symptoms'))
            # session.run("MERGE (c: Causes{Causes: $causes})", causes=item_dict.get('Causes'))
            # session.run("MERGE (dia: Diagnosis{Diagnosis: $diagnosis})", diagnosis=item_dict.get('Diagnosis'))
            # session.run("MERGE (t: Treatment{Treatment: $treatment})", treatment=item_dict.get('Treatment'))
            #
            # # Create relationships
            # session.run("CREATE (MATCH (d:Dieases) WHERE d.diseases = $diseases) - [r: has] -> (MATCH (s:Symptoms) WHERE s.symptoms = $symptoms)", diseases=item_dict.get('Diseases'), symptoms=item_dict.get('Symptoms'))
            # session.run("CREATE (MATCH (d:Dieases) WHERE d.diseases = $diseases) - [r: due_to] -> (MATCH (c:Causes) WHERE c.causes = $causes)", diseases=item_dict.get('Diseases'), causes=item_dict.get('Causes'))
            # session.run("CREATE (MATCH (t:Treatment) WHERE t.treatment = $treatment) - [r: treat] -> (MATCH (d:Dieases) WHERE d.diseases = $diseases)", diseases=item_dict.get('Diseases'), treatment=item_dict.get('Treatment'))




        return item
