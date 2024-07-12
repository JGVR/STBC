# STBCApi
This project is a RESTful API created for Strong Tower Baptist Church (STBC). The api integrates with MongoDb Atlas to perform CRUD operations in a collection with different document schemas. This API was created only for STBC but was designed with the idea that other churches may want to impletement/integrate their own version of this API.

## Getting Started

### Prerequisites
  - Python 3.10

## Installation
### Virtual Environment Set-up
1. Let's set-up a python virtual environment by running the command below:
   * python3.10 -m venv /path/to/new/virtual/environment
2. Activate your virtual environment.
   * source /path/to/new/virtual/environment/bin/activate
3. Run the following command to install all the packages inside the requirements.txt file:
   * pip install -r requirements.txt
   
### Environment Variables
Add the following environment variables to a .env file in the project:
* ATLAS_ADMIN_USER
* ATLAS_ADMIN_PW
* ATLAS_CONN_STR
* ATLAS_DB_NAME
* ATLAS_VECTOR_COLLLECTION

### Docker
If you are using docker, please follow the instructions below:
1. Run the following command to create a docker image:
   * docker build -t "image-name" .
2. Create a container:
   * docker run --name "container-name" --env-file "env-file" "name-of-your-docker-image"

### Atlas Collection Schema
```javascript
{
  "$jsonSchema": {
    "bsonType": "object",
    "required": [
      "_id",
      "type",
      "createdAt"
    ],
    "properties": {
      "_id": {
        "bsonType": "objectId"
      },
      "type": {
        "enum": [
          "church",
          "school",
          "devotion",
          "ministry",
          "event",
          "member",
          "service"
        ],
        "description": "The type field should be one of the following values: church, school, devotion, event, member,ministry, service"
      },
      "createdAt": {
        "bsonType": "date",
        "description": "The createdAt field must be a date field."
      },
      "churchId": {
        "bsonType": "int",
        "description": "The churchId field must an int that uniquely identifies a church."
      }
    },
    "additionalProperties": false,
    "dependencies": {
      "type": {
        "oneOf": [
          {
            "required": [
              "churchId",
              "name"
            ],
            "properties": {
              "type": {
                "enum": [
                  "church"
                ]
              },
              "name": {
                "bsonType": "string",
                "description": "The church name field must be a string no longer than 250 characters.",
                "maxLength": 250
              }
            }
          },
          {
            "required": [
              "churchId",
              "schoolId",
              "name",
              "shortDescription",
              "dateOfWeek",
              "time",
              "classes"
            ],
            "properties": {
              "type": {
                "enum": [
                  "school"
                ]
              },
              "school": {
                "bsonType": "int",
                "description": "The schoolId field must a int that uniquely identifies a school."
              },
              "name": {
                "bsonType": "string",
                "description": "The name field must be a str no longer than 150 characters.",
                "maxLength": 150
              },
              "shortDescription": {
                "bsonType": "string",
                "description": "The shortDescription field must be a string no longer than 500.",
                "maxLength": 500
              },
              "description": {
                "bsonType": [
                  "string",
                  "null"
                ],
                "description": "The school description must be null or a string no longer than 1500 characters.",
                "maxLength": 1500
              },
              "dateOfWeek": {
                "bsonType": "string",
                "description": "The dateOfWeek field must be a string no longer than 10 characters.",
                "maxLength": 10
              },
              "time": {
                "bsonType": [
                  "timestamp",
                  "null"
                ],
                "description": "The school time field must be of a timestamp data type or null."
              },
              "imageUrl": {
                "bsonType": [
                  "string",
                  "null"
                ],
                "description": "The imageUrl field must be a string or null."
              },
              "classes": {
                "bsonType": "array",
                "items": {
                  "bsonType": "object",
                  "description": "The school's classes field must be an array of objects that represents the school's classes.",
                  "required": [
                    "name",
                    "memberId"
                  ],
                  "properties": {
                    "name": {
                      "bsonType": "string",
                      "description": "The name of a class should be a string no longer than 150 characters.",
                      "maxLength": 150
                    },
                    "ages": {
                      "bsonType": "string",
                      "description": "The ages field of a class should a string representing the ages this class is available for. This field should not be longer than 100 characters.",
                      "maxLength": 100
                    },
                    "membersId": {
                      "bsonType": "int",
                      "description": "The membersId field should be an int that uniquely identifies a member of the church."
                    }
                  }
                }
              }
            }
          },
          {
            "required": [
              "churchId",
              "title",
              "date",
              "memberId",
              "message"
            ],
            "properties": {
              "type": {
                "enum": [
                  "devotion"
                ]
              },
              "title": {
                "bsonType": "string",
                "description": "The devotion title field should be a string no longer than 250 characters.",
                "maxLength": 250
              },
              "date": {
                "bsonType": "date",
                "description": "The devotion date field should be a date."
              },
              "message": {
                "bsonType": "string",
                "description": "The devotion message field must be a string."
              },
              "memberId": {
                "bsonType": "int",
                "description": "The devotion memberId field must be an int that uniquely identifies a church member."
              }
            }
          },
          {
            "required": [
              "churchId",
              "title",
              "description",
              "date"
            ],
            "properties": {
              "type": {
                "enum": [
                  "event"
                ]
              },
              "title": {
                "bsonType": "string",
                "description": "The event title field must be a string no longer than 150 characters.",
                "maxLength": 150
              },
              "description": {
                "bsonType": "string",
                "description": "The event description field must be null or a string no longer than 1500 characters.",
                "maxLength": 1500
              },
              "date": {
                "bsonType": "date",
                "description": "The event date field must be a date."
              },
              "imageUrl": {
                "bsonType": [
                  "string",
                  "null"
                ],
                "description": "The event imageUrl field must be null or a string."
              },
              "location": {
                "bsonType": [
                  "null",
                  "string"
                ],
                "description": "The event location field must be null or a string."
              }
            }
          },
          {
            "required": [
              "churchId",
              "memberId",
              "firstName",
              "lastName",
              "title"
            ],
            "properties": {
              "type": {
                "enum": [
                  "member"
                ]
              },
              "memberId": {
                "bsonType": "int",
                "description": "The memberId field must be an int that uniquely identifies a member of the church."
              },
              "firstName": {
                "bsonType": "string",
                "description": "The member's firstName field must be a string no longer than 150 characters.",
                "maxLength": 150
              },
              "middleName": {
                "bsonType": "string",
                "description": "The member's middleName field must be a string no longer than 150 characters.",
                "maxLength": 150
              },
              "lastName": {
                "bsonType": "string",
                "description": "The member's lastName field must be a string no longer than 150 characters.",
                "maxLength": 150
              },
              "title": {
                "bsonType": "string",
                "description": "The member's title field must be a string no longer than 50 characters.",
                "maxLength": 50
              },
              "shortBio": {
                "bsonType": [
                  "string",
                  "null"
                ],
                "description": "The member's shortBio field must be a string no longer than 500 characters.",
                "maxLength": 500
              },
              "imageUrl": {
                "bsonType": [
                  "string",
                  "null"
                ],
                "description": "The member's imageUrl field must be null or a string."
              },
              "startDate": {
                "bsonType": [
                  "null",
                  "date"
                ],
                "description": "The member's startDate field must be null or a date."
              },
              "endDate": {
                "bsonType": [
                  "null",
                  "date"
                ],
                "description": "The member's endDate field must be null or a date."
              }
            }
          },
          {
            "required": [
              "churchId",
              "name",
              "description"
            ],
            "properties": {
              "type": {
                "enum": [
                  "ministry"
                ]
              },
              "name": {
                "bsonType": "string",
                "description": "The ministry's name field must be a string no longer than 100 characters.",
                "maxLength": 100
              },
              "description": {
                "bsonType": "string",
                "description": "The ministry's description field must be a string no longer than 1000 characters.",
                "maxLength": 1000
              },
              "imageUrl": {
                "bsonType": [
                  "string",
                  "null"
                ],
                "description": "The ministry's imageUrl field must be null or a string."
              },
              "registerUrl": {
                "bsonType": [
                  "string",
                  "null"
                ],
                "description": "The ministry's registerUrl field must be null or a string."
              }
            }
          },
          {
            "required": [
              "churchId",
              "title",
              "dateOfWeek",
              "time"
            ],
            "properties": {
              "type": {
                "enum": [
                  "service"
                ]
              },
              "title": {
                "bsonType": "string",
                "description": "The service's name field must be a string no longer than 100 characters.",
                "maxLength": 100
              },
              "dateOfWeek": {
                "bsonType": "string",
                "description": "The service's dateOfWeek field must be a string no longer than 10 characters.",
                "maxLength": 10
              },
              "time": {
                "bsonType": [
                  "timestamp"
                ],
                "description": "The service's time field must be a string."
              }
            }
          }
        ]
      }
    }
  },
  "validationLevel": "strict"
}
```

# Data Design

This section provides a detailed overview of the data design, including the database schema, entity relationships, and security measures implemented to protect the data.

## Overview

The STBC API utilizes two main types of databases to store and manage data efficiently: MongoDB Atlas, a NoSQL database for storing data that belongs to the church.

### Diagrams

#### Model Data Classes UML 
<img width="6720" alt="SBTC Class UML (2)" src="https://github.com/user-attachments/assets/d69e7635-0583-40f1-8601-659032dc5b36">

## Data Security
- Access to read and write data is strictly controlled through role-based access control. Two different user roles are defined: one for reading data and another for both reading and writing data.
- The admin user has exclusive write access to the databases, ensuring that only authorized changes can be made.
- CORS will be also applied at the API and Database level.

# Deployment Strategy
- The API will be deployed in Azure as container apps. 
- CD/CI will be set-up for both API so that any changes to the prod branch in the GitHub repo are automatically deployed to Azure.
