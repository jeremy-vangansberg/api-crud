# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Formation, Rncp, Session as SessionModel


class Cleaning:
    def process_item(self, item, spider):
        item = self.strip_and_list_to_str_all(item)
        item = self.format_code(item)
        return item

    def format_code(self,item):
        adapter = ItemAdapter(item)
        to_strip = ['formacodes_name', 'formacodes_code']
        for key in to_strip: 
            initial_list = adapter.get(key)
            if initial_list :
                cleaned_list = [item.replace(':','').strip() for item in initial_list if item.strip()]
                adapter[key] = cleaned_list
        return item
    







    def strip_and_list_to_str_all(self,item):
        adapter = ItemAdapter(item)
        to_strip = ['location', 'duree', 'dateDebut', 'dateLimiteCandidature', 'sessionName', 'niveau']
        for key in to_strip: 
            value = adapter.get(key)
            if value is not None :
                if not isinstance(value, str):
                    value = "".join(value)
                adapter[key] = value.strip()
        return item
    



class FormationSaving:
    def open_spider(self, spider):
        engine = create_engine('sqlite:///database.db')
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
    
    def process_item(self, item, spider):
        session = self.Session()
        formation = Formation(
            name=item['name'],
            url=item['url']
        )
        session.add(formation)

        formacodes_name = item.get('formacodes_name', [])
        formacodes_code = item.get('formacodes_code', [])

        # Insérer les formacodes dans la table rncp
        for formacode, name in zip(formacodes_name, formacodes_code):
            # Check if the format_code already exists
            existing_rncp = session.query(Rncp).filter_by(format_code=formacode).first()
            if existing_rncp:
                print('------\n', "EXISTING", '------\n', formacode, name)
                formation.rncps.append(existing_rncp)
                # Optionally update the name if needed
                # existing_rncp.name = name
            else:
                rncp = Rncp(
                    format_code=formacode,
                    name=name
                )
                session.add(rncp)
                formation.rncps.append(rncp)
        
        session.commit()
        session.close()
        return item

    def close_spider(self, spider):
        self.Session.close_all()

class SessionSaving:
    def open_spider(self, spider):
        engine = create_engine('sqlite:///database.db')
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        formation = session.query(Formation).filter_by(name=item['name']).first()

        if not formation:
            formation = Formation(
                name=item['name'],
                url=item['url']
            )
            session.add(formation)
            session.commit()  # Commit here to get the formation ID

        session_data = SessionModel(
            formation_id=formation.id_formation,
            session_name=item['sessionName'],
            date_limite_candidature=item['dateLimiteCandidature'],
            alternance=item['alternance'],
            date_debut=item['dateDebut'],
            duree=item['duree'],
            location=item['location'],
            niveau=item['niveau']
        )
        session.add(session_data)
        session.commit()
        session.close()
        return item

    def close_spider(self, spider):
        self.Session.close_all()