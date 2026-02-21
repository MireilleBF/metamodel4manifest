"""
This module defines the Artefact class and its subclasses,
which represent different types of artefacts in the context of software development
and data management.
The Artefact class serves as a base class for specific types of artefacts,
such as Person and SoftwareFile, which have additional properties and validation rules.
"""

import mimetypes
from dataclasses import dataclass, field
from typing import Optional, List

from DSL4Pipelines.src.metamodel.catalogs.artefact_catalog import ArtefactCatalog
from DSL4Pipelines.src.metamodel.catalogs.SoftwareCatalog import SoftwareCatalog
from DSL4Pipelines.src.metamodel.core.structure import Element, ExternalReference
from DSL4Pipelines.src.metamodel.catalogs.vocabulary import FileKind

# Initialize the mimetypes module to ensure that the types are loaded and available for validation
mimetypes.init()


@dataclass
class Artefact(Element):
    """
    The Artefact class represents a general artefact with common properties such as
     access, license, type, and category.
    """

    access: Optional[str] = (
        None  # e.g., ArtefactCatalog.ACCESS.PUBLIC, ArtefactCatalog.ACCESS.PRIVATE, etc.
    )
    license: Optional[str] = (
        None  # e.g., SPDX license identifier like "MIT", "GPL-3.0-only", etc.
    )
    type: str = "Artefact"
    category: Optional[str] = (
        None  # e.g., ArtefactCatalog.CATEGORY.DATASET, ArtefactCatalog.CATEGORY.SOFTWARE, etc.
    )

    # ne fonctionne pas par heritage ou appel à super...
    def __post_init__(self):
        # When the object is created, if the type is not explicitly set,
        # we can set it to the name of the class by default.
        if self.type is None:
            # We can use the class name as the default type, but it can be overridden if needed.
            self.type = self.__class__.__name__

    def validate(self, errors: Optional[list] = None) -> bool:
        """Validate the artefact properties, such as access and license."""
        # Basic validation for common artefact properties
        access_ok = True
        if self.access is not None:
            access_ok = self.access in ArtefactCatalog.ACCESS.ALL

        if not access_ok:
            message = (
                f"access '{self.access}' is not recognized. "
                f"Valid options are: {ArtefactCatalog.ACCESS.ALL}"
            )
            if errors is not None:
                errors.append(message)
            else:
                errors = [message]

        # License validation could be more complex,
        # but for now we can just check if it's a non-empty string or a known SPDX identifier.
        license_ok = True
        if self.license is not None:
            license_ok = (
                isinstance(self.license, str) and len(self.license) > 0
            )  # Simple check for non-empty string
            if not license_ok:
                message = f"license '{self.license}' is not valid. It should be a non-empty string."
                if errors is not None:
                    errors.append(message)
                else:
                    errors = [message]

        return access_ok and license_ok


@dataclass
class Person(Artefact):
    """From SPDX (simplified) The Person class represents an individual person
    with a list of external identifiers."""

    external_identifier: List[ExternalReference] = field(default_factory=list)


@dataclass
class SoftwareFile(Artefact):
    """The SoftwareFile class represents a software file artefact, (from SPDX)
    which is a specific type of artefact with additional properties related to software files."""

    type: str = "SoftwareFile"  # Override the type to specify that this is a SoftwareFile artifact
    software_file_kind: FileKind = FileKind.FILE
    software_primary_purpose: Optional[str] = None
    content_type: Optional[str] = None
    release_time: Optional[str] = None
    software_copyright_text: Optional[str] = None
    software_download_location: Optional[str] = None
    external_reference: Optional[ExternalReference] = (
        None  # MI: added an optional attribute to link to an external reference
        # (e.g., a URL or a database entry) that provides more information about the software file.
    )
    languages: List[str] = field(
        default_factory=list
    )  # MI added can mix description and implementation

    @staticmethod
    def _is_valid_mime(mime_str: str) -> bool:
        # 1. First, we check if the string has the basic structure of a MIME type (type/subtype)
        if "/" not in mime_str or mime_str.startswith("/") or mime_str.endswith("/"):
            return False

        # 2. Get the main type and subtype
        known_types = set(mimetypes.types_map.values())
        # Additionally, we can also consider the common types
        # that might not be in the main map but are still valid MIME types.
        known_types.update(mimetypes.common_types.values())
        return mime_str in known_types

    def validate(self, errors: list = None) -> bool:
        # 1. first we call the superclass validation to check for common artefact properties
        base_valid = super().validate(errors)

        # 2. Add specific validation for SoftwareFile properties
        mime_ok = True
        if self.content_type:
            mime_ok = SoftwareFile._is_valid_mime(self.content_type)
        if not mime_ok:
            # add an error message to the errors list
            message = f"Validation error: contentType '{self.content_type}' is not a valid MIME type."
            if errors is not None:
                errors.append(message)
            else:
                errors = [message]

            # print(f"Validation error: contentType '{self.contentType}' is not a valid MIME type.")

        allowed_languages = (
            SoftwareCatalog.LANGUAGES.CODE
            + SoftwareCatalog.LANGUAGES.FORMATS
            + SoftwareCatalog.LANGUAGES.NATURAL
        )

        languages_ok = all(lang in allowed_languages for lang in self.languages)
        if not languages_ok:
            message = f"Validation error: One or more languages in {self.languages} are not in the allowed list of languages : {allowed_languages}."
            if errors is not None:
                errors.append(message)
            else:
                errors = [message]

        return base_valid and mime_ok and languages_ok


"""
            
{
    "@context": "https://spdx.org/rdf/3.0.1/spdx-context.jsonld",
    "@graph": [
        {
            "@id": "_:creationinfo",
            "created": "2024-11-06T19:30:00Z",
            "createdBy": [
                "https://orcid.org/0000-0002-9698-1899"
            ],
            "specVersion": "3.0.1",
            "type": "CreationInfo"
        },
        {
            "creationInfo": "_:creationinfo",
            "externalIdentifier": [
                {
                    "externalIdentifierType": "other",
                    "identifier": "bact",
                    "identifierLocator": [
                        "https://github.com/bact/"
                    ],
                    "issuingAuthority": "GitHub",
                    "type": "ExternalIdentifier"
                }
            ],
            "name": "Arthit Suriyawongkul",
            "spdxId": "https://orcid.org/0000-0002-9698-1899",
            "type": "Person"
        },
        {
            "creationInfo": "_:creationinfo",
            "externalIdentifier": [
                {
                    "externalIdentifierType": "other",
                    "identifier": "PyThaiNLP",
                    "identifierLocator": [
                        "https://github.com/PyThaiNLP/"
                    ],
                    "issuingAuthority": "GitHub",
                    "type": "ExternalIdentifier"
                }
            ],
            "name": "PyThaiNLP",
            "spdxId": "https://pythainlp.org/",
            "type": "Organization"
        },
        {
            "creationInfo": "_:creationinfo",
            "externalIdentifier": [
                {
                    "externalIdentifierType": "other",
                    "identifier": "wisesight",
                    "identifierLocator": [
                        "https://github.com/wisesight/"
                    ],
                    "issuingAuthority": "GitHub",
                    "type": "ExternalIdentifier"
                }
            ],
            "name": "Wisesight (Thailand) Co., Ltd.",
            "spdxId": "https://wisesight.com/",
            "type": "Organization"
        },
        {
            "creationInfo": "_:creationinfo",
            "profileConformance": [
                "core",
                "dataset"
            ],
            "rootElement": [
                "https://spdx.org/spdxdocs/Bom/01-5b1aeec4-be22-44dc-ae37-4594e38e5119"
            ],
            "spdxId": "https://spdx.org/spdxdocs/SpdxDocument/01-969f4a32-c67c-4824-8afa-d9ac8e634b75",
            "type": "SpdxDocument"
        },
        {
            "creationInfo": "_:creationinfo",
            "profileConformance": [
                "core",
                "dataset"
            ],
            "rootElement": [
                "https://spdx.org/spdxdocs/DatasetPackage/01-c69d31e2-43cd-4918-ab26-71f198a85cd1"
            ],
            "spdxId": "https://spdx.org/spdxdocs/Bom/01-5b1aeec4-be22-44dc-ae37-4594e38e5119",
            "type": "Bom"
        },
        {
            "builtTime": "2024-11-06T17:30:00Z",
            "comment": "See more at: https://github.com/PyThaiNLP/wisesight-sentiment/blob/master/README.md",
            "creationInfo": "_:creationinfo",
            "dataset_anonymizationMethodUsed": [
                "masking",
                "removal"
            ],
            "dataset_confidentialityLevel": "clear",
            "dataset_dataCollectionProcess": "Data was collected from approximately 2016 to early 2019, with a small amount from other periods. Collection was made only from messages that made available to the public on the internet (websites, blogs, social network sites). For Facebook, this means the public comments (everyone can see) that made on a public page. Private/protected messages and messages in groups, chat, and inbox are not included.",
            "dataset_dataPreprocessing": [
                "Large amount of messages are not in their original form. Personal data are removed or masked.",
                "Usernames and non-public figure names are removed.",
                "Phone numbers are masked (e.g., 088-888-8888, 09-9999-9999, 0-2222-2222).",
                "Duplicated, leading, and trailing whitespaces are removed. Other punctuations, symbols, and emojis are kept intact.",
                "(Mis)spellings are kept intact.",
                "Messages longer than 2,000 characters are removed.",
                "Long non-Thai messages are removed. Duplicated message (exact match) are removed.",
                "Sentiment value annotation is added, using the following methodology.",
                "Sentiment values are assigned by human annotators.",
                "A human annotator put his/her best effort to assign just one label, out of four, to a message.",
                "A message can be ambiguous. When possible, the judgement will be based solely on the text itself.",
                "In some situation, like when the context is missing, the annotator may have to rely on his/her own world knowledge and just guess.",
                "In some cases, the human annotator may have access to the message's context, like an image. These additional information are not included as part of this corpus.",
                "Agreement, enjoyment, and satisfaction are positive. Disagreement, sadness, and disappointment are negative.",
                "Showing interest in a topic or in a product is counted as positive.",
                "In this sense, a question about a particular product could have a positive sentiment value, if it shows the interest in the product.",
                "Saying that other product or service is better is counted as negative.",
                "General information or news title tend to be counted as neutral."
            ],
            "dataset_datasetAvailability": "directDownload",
            "dataset_datasetSize": 6325249,
            "dataset_datasetType": [
                "categorical",
                "text"
            ],
            "dataset_datasetUpdateMechanism": "manual",
            "dataset_hasSensitivePersonalInformation": "no",
            "dataset_intendedUse": "For training and evaluation of sentiment analysis models.",
            "dataset_knownBias": [
                "The corpus does not statistically represent the language register or the proportion of diverse Thai dialects.",
                "The primary language of this corpus is Central Thai.",
                "Due to the nature of social media, the language style tends to be informal and conversational.",
                "However, it also contains some more formal language from news headlines and advertisements.",
                "The domains are mixed, with the majority being consumer products and services (restaurants, cosmetics, drinks, cars, hotels), and a smaller portion consisting of current affairs."
            ],
            "description": "Social media messages in Thai language with sentiment label (positive, neutral, negative, question). Contains 26,737 messages. Released to public domain under Creative Commons Zero v1.0 Universal license. More characteristics of the data can be explored by this notebook: https://github.com/PyThaiNLP/wisesight-sentiment/blob/master/exploration.ipynb.",
            "name": "PyThaiNLP/Wisesight Sentiment Corpus with Word Tokenization Label",
            "originatedBy": [
                "https://pythainlp.org/",
                "https://wisesight.com/"
            ],
            "releaseTime": "2024-11-06T19:30:00Z",
            "software_copyrightText": "Dedicated to the public domain under CC0 1.0 Universal by Wisesight (Thailand) Co., Ltd. and PyThaiNLP project.",
            "software_downloadLocation": "https://github.com/PyThaiNLP/wisesight-sentiment/releases",
            "software_homePage": "https://github.com/PyThaiNLP/wisesight-sentiment/",
            "software_packageVersion": "1.1",
            "software_primaryPurpose": "data",
            "spdxId": "https://spdx.org/spdxdocs/DatasetPackage/01-c69d31e2-43cd-4918-ab26-71f198a85cd1",
            "summary": "Social media messages in Thai language with sentiment label. Contains 26,737 messages.",
            "type": "dataset_DatasetPackage"
        },
        {
            "contentType": "text/plain;charset=UTF-8",
            "creationInfo": "_:creationinfo",
            "name": "LICENSE",
            "originatedBy": [
                "https://pythainlp.org/"
            ],
            "releaseTime": "2020-05-20T20:00:00Z",
            "software_primaryPurpose": "documentation",
            "spdxId": "https://spdx.org/spdxdocs/File/01-0710b717-a9c1-41de-af42-f41827c30ccc",
            "summary": "License file for the dataset, which is CC0 1.0 Universal.",
            "type": "software_File"
        },
        {
            "contentType": "text/plain;charset=UTF-8",
            "creationInfo": "_:creationinfo",
            "name": "neg.txt",
            "originatedBy": [
                "https://wisesight.com/"
            ],
            "releaseTime": "2019-03-31T20:00:00Z",
            "software_primaryPurpose": "data",
            "spdxId": "https://spdx.org/spdxdocs/File/02-32d6319e-e619-42f8-8834-15792c780e7c",
            "summary": "Negative sentiment messages. 14,561 messages.",
            "type": "software_File"
        },
        {
            "contentType": "text/plain;charset=UTF-8",
            "creationInfo": "_:creationinfo",
            "name": "neu.txt",
            "originatedBy": [
                "https://wisesight.com/"
            ],
            "releaseTime": "2019-03-31T20:00:00Z",
            "software_primaryPurpose": "data",
            "spdxId": "https://spdx.org/spdxdocs/File/03-c2ba0c57-d1fd-4fad-8daa-227f86e62d70",
            "summary": "Neutral sentiment messages. 6,823 messages.",
            "type": "software_File"
        },
        {
            "contentType": "text/plain;charset=UTF-8",
            "creationInfo": "_:creationinfo",
            "name": "pos.txt",
            "originatedBy": [
                "https://wisesight.com/"
            ],
            "releaseTime": "2019-03-31T20:00:00Z",
            "software_primaryPurpose": "data",
            "spdxId": "https://spdx.org/spdxdocs/File/04-743ce7f8-b4a6-476f-bf3a-eb10bea3d3b2",
            "summary": "Positive sentiment messages. 4,778 messages",
            "type": "software_File"
        },
        {
            "contentType": "text/plain;charset=UTF-8",
            "creationInfo": "_:creationinfo",
            "name": "q.txt",
            "originatedBy": [
                "https://wisesight.com/"
            ],
            "releaseTime": "2019-03-31T20:00:00Z",
            "software_primaryPurpose": "data",
            "spdxId": "https://spdx.org/spdxdocs/File/05-c9bfbf0d-8993-4a5c-ab98-22bd2e1044b6",
            "summary": "Question messages. 575 messages.",
            "type": "software_File"
        },
        {
            "contentType": "text/plain;charset=UTF-8",
            "creationInfo": "_:creationinfo",
            "name": "README.md.md",
            "originatedBy": [
                "https://pythainlp.org/"
            ],
            "releaseTime": "2024-11-06T19:30:00Z",
            "software_primaryPurpose": "documentation",
            "spdxId": "https://spdx.org/spdxdocs/File/06-c79a169b-df75-4a01-aa8b-713a5dc86441",
            "summary": "README.md file for the dataset. Contains information about the dataset, its collection process, and its annotation methodology.",
            "type": "software_File"
        },
        {
            "creationInfo": "_:creationinfo",
            "from": "https://spdx.org/spdxdocs/DatasetPackage/01-c69d31e2-43cd-4918-ab26-71f198a85cd1",
            "relationshipType": "contains",
            "spdxId": "https://spdx.org/spdxdocs/Relationship/contains-01-805ea98f-16a4-4b37-b706-387403d39d2d",
            "summary": "DatasetPackage/01 contains LICENSE, neg.txt, neu.txt, pos.txt, q.txt, and README.md.md.",
            "to": [
                "https://spdx.org/spdxdocs/File/01-0710b717-a9c1-41de-af42-f41827c30ccc",
                "https://spdx.org/spdxdocs/File/02-32d6319e-e619-42f8-8834-15792c780e7c",
                "https://spdx.org/spdxdocs/File/03-c2ba0c57-d1fd-4fad-8daa-227f86e62d70",
                "https://spdx.org/spdxdocs/File/04-743ce7f8-b4a6-476f-bf3a-eb10bea3d3b2",
                "https://spdx.org/spdxdocs/File/05-c9bfbf0d-8993-4a5c-ab98-22bd2e1044b6",
                "https://spdx.org/spdxdocs/File/06-c79a169b-df75-4a01-aa8b-713a5dc86441"
            ],
            "type": "Relationship"
        },
        {
            "creationInfo": "_:creationinfo",
            "from": "https://spdx.org/spdxdocs/File/06-c79a169b-df75-4a01-aa8b-713a5dc86441",
            "relationshipType": "describes",
            "spdxId": "https://spdx.org/spdxdocs/Relationship/describes-01-d8785f35-497b-4e0a-8fac-d4eede982e4e",
            "summary": "README.md.md describes neg.txt, neu.txt, pos.txt, and q.txt.",
            "to": [
                "https://spdx.org/spdxdocs/File/02-32d6319e-e619-42f8-8834-15792c780e7c",
                "https://spdx.org/spdxdocs/File/03-c2ba0c57-d1fd-4fad-8daa-227f86e62d70",
                "https://spdx.org/spdxdocs/File/04-743ce7f8-b4a6-476f-bf3a-eb10bea3d3b2",
                "https://spdx.org/spdxdocs/File/05-c9bfbf0d-8993-4a5c-ab98-22bd2e1044b6"
            ],
            "type": "Relationship"
        },
        {
            "creationInfo": "_:creationinfo",
            "from": "https://spdx.org/spdxdocs/DatasetPackage/01-c69d31e2-43cd-4918-ab26-71f198a85cd1",
            "relationshipType": "hasConcludedLicense",
            "spdxId": "https://spdx.org/spdxdocs/Relationship/concludedLicense-01-3cfe0c7d-1a2d-4609-b468-0b2c2ed50501",
            "summary": "DatasetPackage/01 has a concluded license as CC0-1.0.",
            "to": [
                "https://spdx.org/licenses/CC0-1.0"
            ],
            "type": "Relationship"
        },
        {
            "creationInfo": "_:creationinfo",
            "from": "https://spdx.org/spdxdocs/DatasetPackage/01-c69d31e2-43cd-4918-ab26-71f198a85cd1",
            "relationshipType": "hasDeclaredLicense",
            "spdxId": "https://spdx.org/spdxdocs/Relationship/declaredLicense-01-fbc5f8d0-e7ab-45a2-b5b5-1cabe6e697ac",
            "summary": "DatasetPackage/01 has a declared license as CC0-1.0.",
            "to": [
                "https://spdx.org/licenses/CC0-1.0"
            ],
            "type": "Relationship"
        }
    ]
}
"""
