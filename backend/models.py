from cms.models.pluginmodel import CMSPlugin
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models
import uuid

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
    collection_id = models.CharField(max_length=200, default='library_id')
    style= models.CharField(max_length=200, default='apa')
    html=models.JSONField(editable=False)
    unique_identifier=models.UUIDField(default=uuid.uuid4, editable=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add your own logic
        # zotero_base_url = 'https://api.zotero.org'/groups/2834237/collections/VR8U3MFZ/items?format=json&include=bib,data&style=apa&key=Br5u8p81bg4nGJMH7Mti9Qag
        html={
            "bib":[
                "<div class=\"csl-bib-body\" style=\"line-height: 2; padding-left: 1em; text-indent:-1em;\">\n  <div class=\"csl-entry\">Maidment, D. R. (2005). <i>Hydrologic Information System Status Report</i>. CUAHSI. https://hydrology.usu.edu/dtarb/HISStatusSept15.pdf</div>\n</div>",
                "<div class=\"csl-bib-body\" style=\"line-height: 2; padding-left: 1em; text-indent:-1em;\">\n  <div class=\"csl-entry\">Elkin Giovanni Romero Bustamante, E. James Nelson, Ames, D. P., Gustavious Williams, Norm Jones, Boldrini, E., &amp; Chernov, I. (2021). <i>Water Data Explorer</i> (1.1.0). Zenodo. https://doi.org/10.5281/ZENODO.4678966</div>\n</div>"
            ]
        }
        self.html = html