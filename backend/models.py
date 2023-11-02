from cms.models.pluginmodel import CMSPlugin
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models
from pyzotero import zotero
import datetime
import uuid
from django.db.models.signals import pre_save
from django.dispatch import receiver


class HydroShareResource(CMSPlugin):
    title = models.CharField(max_length=200, default='resource title')
    subtitle = models.CharField(max_length=200, default='resource subtitle')
    image = models.CharField(max_length=200, default='https://picsum.photos/200')
    width= models.PositiveIntegerField(default=200, validators=[MinValueValidator(150), MaxValueValidator(400)])
    height=models.PositiveIntegerField(default=200, validators=[MinValueValidator(150), MaxValueValidator(400)])
    description= models.TextField(default='resource description')
    github_url=models.CharField(max_length=200, default='', blank=True)
    documentation_url=models.CharField(max_length=200, default='', blank=True)
    web_site_url=models.CharField(max_length=200, default='', blank=True)
    unique_identifier=models.UUIDField(default=uuid.uuid4, editable=False)

# class ZoteroCitationResource(CMSPlugin):
#     authors = models.CharField(max_length=200, default='Publication Authors')
#     date=models.CharField(max_length=200, default='Publication Date')
#     title = models.CharField(max_length=200, default='Publication Title')
#     publication = models.CharField(max_length=200, default='Publication Title/Publisher Title')
#     doi=models.CharField(max_length=200, default='Publication DOI')
#     unique_identifier=models.UUIDField(default=uuid.uuid4, editable=False)

class ZoteroBibliographyResource(CMSPlugin):
    api_key = models.CharField(max_length=200, default='api_key')
    library_type=models.CharField(max_length=200, default='user')
    library_id = models.CharField(max_length=200, default='library_id')
    collection_id = models.CharField(max_length=200, default='collection_id', blank=True)
    style= models.CharField(max_length=200, default='apa')
    html=models.JSONField(editable=False)
    unique_identifier=models.UUIDField(default=uuid.uuid4, editable=False)
    
    
@receiver(pre_save, sender=ZoteroBibliographyResource)
def create_html_citations(sender, instance, *args, **kwargs):

    zot = zotero.Zotero(instance.library_id, instance.library_type, instance.api_key)
    include_fields='bib,data'
    print(instance.collection_id)
    # if instance.collection_id != 'collection_id' and  instance.collection_id:
    #     items = zot.collection_items(collectionID=instance.collection_id, style=instance.style, include=include_fields)
    # else:
    items = zot.items(style=instance.style, include=include_fields, sort="date")
    # 2080-03 was put ion order to have the publications without date at the end
    # items = sorted(items, key=lambda item:datetime.datetime.strptime(item['meta'].get('parsedDate','2080-03').split('-')[0], "%Y"))

    # Initialize a dictionary to store publications by year
    publications_by_year = {}

    # Iterate through the data and populate the dictionary
    for item in items:
        # Extract the year from "parsedDate" (if available)
        parsed_date = item.get("meta", {}).get("parsedDate", "")
        year = parsed_date.split("-")[0] if parsed_date else "More Publications"

        # Add the publication to the corresponding year's list
        if year not in publications_by_year:
            publications_by_year[year] = []
        publications_by_year[year].append(item["bib"])

    print(publications_by_year)
    # html_list = [item["bib"] for item in items]

    html={
        "bib":publications_by_year
    }
    instance.html = publications_by_year     