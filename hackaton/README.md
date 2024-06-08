## Endpoints

### localhost:8000/connect/
```json
{
  "databaseType": "postgreSQL",
  "url": "147.45.226.188",
  "port": "5432",
  "user": "hackathon",
  "password": "28g8Lh5-yLHR",
  "copy": false
}
```
### localhost:8000/update-columns/
input data example
```json
{
	"employee": {
		"id": true
	}
}
```
output data example
```json
{
	"jobs": {
//      ...
	},
	"departments": {
//      ...
	},
	"highscools": {
//      ...
	},
	"directions": {
//      ...
	},
	"addresses": {
//      ...
	},
	"rf_cities": {
//      ...
	},
	"sections": {
//      ...
	},
	"mil_specs": {
//      ...
	},
	"pays": {
//      ...
	},
	"paytypes": {
//      ...
	},
	"rf_subjects": {
//      ...
	},
	"rf_regions": {
//        ...
	},
	"mil_ranks": {
//      ...
	},
	"diplomas": {
//      ...
	},
	"specialites": {
//    ...
	},
	"militaries": {
//      ...
	},
	"employee": {
		"id": true,
		"dept": false,
		"dir": false,
//      ...
	}
}
```