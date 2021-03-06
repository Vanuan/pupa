"""
    Schema for event objects.
"""

from .common import sources, extras

media_schema = {
    "description": ("This \"special\" schema is used in two places in the Event"
                    " schema, on the top level and inside the agenda item. This is an"
                    " optional component that may be omited entirely from a document."),
    "items": {
        "properties": {
            "name": {
                "type": "string",
                "description": ('name of the media link, such as "Recording of'
                                ' the meeting" or "Discussion of construction'
                                ' near the watershed"'),
            },

            "type": {
                "type": "string",
                "description": ('type of the set of recordings, such as'
                                ' "recording" or "testimony".'),
            },

            "date": {
                "pattern": "^([0-9]{4})?(-[0-9]{2}){0,2}$",
                "type": "string", "blank": True,
                "description": "date of the recording.",
            },

            "offset": {
                "type": ["number", "null"],
                "description": ("Offset where the related part starts. This is"
                                " optional and may be ommited entirely."),
            },

            "links": {
                "description": ("List of links to the same media item, each"
                                " with a different media_type."),
                "items": {
                    "properties": {
                        "media_type": {
                            "description": ("media type of the media, such"
                                            " as video/mp4 or audio/webm"),
                            "type": ["string", "null"]
                        },

                        "url": {
                            "type": "string",
                            "description": "URL where this media may be accessed",
                        },

                    },
                    "type": "object"
                },
                "type": "array"
            },
        },
        "type": "object"
    },
    "type": "array"
}

schema = {
    "description": "event data",

    "_order": (
        ('Basics', ('name', 'description', 'when', 'end', 'status', 'location')),
        ('Linked Entities', ('media', 'links', 'participants', 'agenda', 'documents',)),
        ('Common Fields', ['updated_at', 'created_at', 'sources']),
    ),

    "properties": {
        "name": {
            "type": "string",
            "description": ('A simple name of the event, such as "Fiscal'
                            ' subcommittee hearing on pudding cups"')
        },

        "all_day": {
            "type": ["boolean"],
            "description": ("Indicates if the event is an all-day event"),
        },

        "classification": {
            "type": ["string"],
            "description": ("type of event"),
        },
        # TODO: turn into enum

        "updated_at": {
            "type": ["string", "datetime"],
            "required": False,
            "description": "the time that this object was last updated.",
        },

        "created_at": {
            "type": ["string", "datetime"],
            "required": False,
            "description": "the time that this object was first created.",
        },

        "description": {
            "type": "string", "blank": True,
            "description": ('A longer description describing the event. As an'
                            ' example, "Topics for discussion include this that'
                            ' and the other thing. In addition, lunch will be'
                            ' served".'),
        },

        "start_time": {
            "type": ["datetime"],
            "description": ("Starting date / time of the event. This should be"
                            " fully timezone qualified."),
        },

        "end_time": {
            "type": ["datetime", "null"],
            "description": ("Ending date / time of the event. This should"
                            " be fully timezone qualified."),
        },


        "status": {
            "type": "string", "blank": True,
            "enum": ["cancelled", "tentative", "confirmed", "passed"],
            "description": ("String that denotes the status of the meeting."
                            " This is useful for showing the meeting is cancelled"
                            " in a machine-readable way."),
        },

        "location": {
            "description": "Where the event will take place.",
            "type": "object",
            "properties": {

                "name": {
                    "type": "string",
                    "description": ('name of the location, such as "City Hall,'
                                    ' Boston, MA, USA", or "Room E201, Dolan'
                                    ' Science Center, 20700 North Park Blvd'
                                    ' University Heights Ohio, 44118"'),
                },

                "note": {
                    "type": "string", "blank": True,
                    "description": ('human readable notes regarding the location,'
                                    ' something like "The meeting will take place'
                                    ' at the Minority Whip\'s desk on the floor"')
                },

                "url": {
                    "required": False,
                    "type": "string",
                    "description": "URL of the location, if applicable.",
                },

                "coordinates": {
                    "description": ('coordinates where this event will take'
                                    ' place. If the location hasn\'t (or isn\'t)'
                                    ' geolocated or geocodable, than this should'
                                    ' be set to null.'),
                    "type": ["object", "null"],
                    "properties": {
                        "latitude": {
                            "type": "string",
                            "description": "latitude of the location, if any",
                        },

                        "longitude": {
                            "type": "string",
                            "description": "longitude of the location, if any",
                        }
                    }
                },
            },
        },

        "media": media_schema,

        "documents": {
            "description": ("Links to related documents for the event. Usually,"
                            " this includes things like pre-written testimony,"
                            " spreadsheets or a slide deck that a presenter will"
                            " use."),
            "items": {
                "properties": {
                    "name": {
                        "type": "string",
                        "description": ('name of the document. Something like'
                                        ' "Fiscal Report" or "John Smith\'s'
                                        ' Slides".'),
                    },

                    "url": {
                        "type": "string",
                        "description": "URL where the content may be found.",
                    },

                    "media_type": {
                        "type": "string",
                        "description": "Mimetype of the document.",
                    },
                },
                "type": "object"
            },
            "type": "array"
        },

        "links": {
            "description": ("Links related to the event that are not documents"
                            " or items in the Agenda. This is filled with helpful"
                            " links for the event, such as a committee's homepage,"
                            " reference material or links to learn more about subjects"
                            " related to the event."),
            "items": {
                "properties": {

                    "note": {
                        "description": ('Human-readable name of the link. Something'
                                        ' like "Historical precedent for popsicle procurement"'),
                        "type": "string",
                        "blank": True,
                    },

                    "url": {
                        "description": "A URL for a link about the event",
                        "format": "uri",
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        },

        "participants": {
            "description": ("List of participants in the event. This includes"
                            " committees invited, legislators chairing the event"
                            " or people who are attending."),
            "items": {
                "properties": {

                    "name": {
                        "type": "string",
                        "description": "Human readable name of the entitity.",
                    },

                    "id": {
                        "type": ["string", "null"],
                        "description": "ID of the participant",
                    },

                    "type": {
                        "enum": ["organization", "person"],
                        "type": "string",
                        "description": ("What type of entity is this? `person`"
                                        " may be used if the person is not a Legislator,"
                                        " butattending the event, such as an"
                                        " invited speaker or one who is offering"
                                        " testimony."),
                    },

                    "note": {
                        "type": "string",
                        "description": ("Note regarding the relationship, such"
                                        " as `chair` for the chair of a meeting."),
                    },

                },
                "type": "object"
            },
            "type": "array"
        },

        "agenda": {
            "description": ("Agenda of the event, if any. This contains information"
                            " about the meeting's agenda, such as bills to"
                            " discuss or people to present."),
            "items": {
                "properties": {
                    "description": {
                        "type": "string",

                        "description": ("Human-readable string that represents this"
                                        " agenda item. A good example would be something like"
                                        " The Committee will consider SB 2339, HB 100"),
                    },

                    "order": {
                        "type": ["string", "null"],
                        "description": ("order of this item, useful for re-creating"
                                        " meeting minutes. This may be ommited entirely."
                                        " It may also optionally contains \"dots\""
                                        " to denote nested agenda items, such as \"1.1.2.1\""
                                        " or \"2\", which may go on as needed."),
                    },

                    "subjects": {
                        "description": ("List of related topics of this agenda"
                                        " item relates to."),
                        "items": {"type": "string"},
                        "type": "array"
                    },

                    "media": media_schema,

                    "notes": {
                        "description": ("Notes taken during this agenda"
                                        " item, may be used to construct meeting minutes."),
                        "type": "string", "blank": True,
                    },

                    "related_entities": {
                        "description": ("Entities that relate to this agenda"
                                        " item, such as presenters, legislative"
                                        " instruments, or committees."),
                        "items": {
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "description": ("type of the related object, like"
                                                    " `bill` or `organization`."),
                                },

                                "id": {
                                    "type": ["string", "null"],
                                    "description": "ID of the related entity",
                                },

                                "name": {
                                    "type": "string",
                                    "description": ("human readable string"
                                                    " representing the entity,"
                                                    " such as `John Q. Smith`."),
                                },

                                "note": {
                                    "type": ["string", "null"],
                                    "description": ("human readable string (if any) noting"
                                                    " the relationship between the entity and"
                                                    " the agenda item, such as \"Jeff"
                                                    " will be presenting on the effects"
                                                    " of too much cookie dough\""),
                                },
                            },
                            "type": "object",
                        },
                        "minItems": 0,
                        "type": "array",
                    },
                },
                "type": "object"
            },
            "minItems": 0,
            "type": "array"
        },
        "sources": sources,
        "extras": extras,
    },
    "type": "object"
}
