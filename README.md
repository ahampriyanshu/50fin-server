# 50Fin Server

- [https://five0fin.onrender.com/docs](https://five0fin.onrender.com/docs)
- [https://five0fin.onrender.com/redoc](https://five0fin.onrender.com/redoc)

## Setup

```bash
git clone https://github.com/ahampriyanshu/50fin-server.git 50fin-server
cd 50fin-server
pip3 install -r requirements.txt
```

- Setup and run postgres server
- Update the .env variables
- Run `uvicorn main:app --reload`

## Endpoints

- [https://five0fin.onrender.com/api](https://five0fin.onrender.com/api)

### Responses

#### 200, 201, 204

Single Response

```
{
id: uuid
title: string
body: text
slug: string
created_at: datetime
updated_at: datetime
}
```

Batched Response
```
{
"data": {
,
"next":{

},
"next":{
    
}
}
```

List Response
```
{
"data": [ ],
"metadata": {
"results": 0,
"limit": 0,
"page":0,
}
}
```

#### 400, 404, 405, 409, 422, 500

```
{
    "error_message" : ""
}
```