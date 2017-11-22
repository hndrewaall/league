up:
	docker-compose -f docker-compose.yml -f docker-compose-debug-override.yml up --build

nuke-db:
	docker-compose stop db && docker-compose rm -f db && docker volume rm league_db_data && docker-compose -f docker-compose.yml -f docker-compose-debug-override.yml up -d --build

upd:
	docker-compose -f docker-compose.yml -f docker-compose-debug-override.yml up --build -d
