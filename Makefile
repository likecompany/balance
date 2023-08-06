# ============================================VARIABLES===========================================
docker_v2 = docker compose

application_directory = app
compose_directory = docker/compose
tests_directory = tests
code_directory = $(application_directory) $(tests_directory)

alembic_container = $(compose_directory)/alembic.yml
application_container = $(compose_directory)/app.yml
database_container = $(compose_directory)/db.yml
main_container = $(compose_directory)/main.yml
network_container = $(compose_directory)/networks.yml
tests_database_container = $(compose_directory)/tests.db.yml
tests_container = $(compose_directory)/tests.yml

capture_exit_code = --abort-on-container-exit --exit-code-from
exit_code_tests = balance_tests
exit_code_migrations = balance_alembic

compose_application = $(docker_v2) -f $(main_container) -f $(network_container) -f $(application_container) -f $(database_container) --env-file .env
compose_tests = $(docker_v2) -f $(main_container) -f $(network_container) -f $(tests_container) -f $(tests_database_container) --env-file .env
compose_migrations = $(docker_v2) -f $(main_container) -f $(network_container) -f $(alembic_container) -f $(database_container) --env-file .env
# ============================================VARIABLES===========================================

# =============================================SYSTEM=============================================
.PHONY: clean
clean:
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf {.cache,.ruff_cache,.mypy_cache,.coverage,htmlcov,.pytest_cache}
# =============================================SYSTEM=============================================

# ==============================================CODE==============================================
.PHONY: lint
lint:
	isort --check-only $(code_directory)
	black --check --diff $(code_directory)
	ruff $(code_directory)
	mypy $(application_directory)

.PHONY: reformat
reformat:
	black $(code_directory)
	isort $(code_directory)
	ruff --fix $(code_directory)
# ==============================================CODE==============================================

# ======================================DOCKER(COMMON RULES)======================================
.PHONY: build
build:
	$(compose_application) build
	$(compose_tests) build
	$(compose_migrations) build

.PHONY: stop
stop:
	$(compose_application) stop
	$(compose_tests) stop
	$(compose_migrations) stop

.PHONY: down
down:
	$(compose_application) down
	$(compose_tests) down
	$(compose_migrations) down

.PHONY: destroy
destroy:
	$(compose_application) down -v
	$(compose_tests) down -v
	$(compose_migrations) down -v

.PHONY: exec
exec:
	$(compose_application) exec $(container) /bin/bash
# ======================================DOCKER(COMMON RULES)======================================

# ==========================================DOCKER(APP)===========================================
.PHONY: build-application
build-application:
	$(compose_application) build

.PHONY: application
application:
	$(compose_application) up -d

.PHONY: stop-application
stop-application:
	$(compose_application) stop

.PHONY: down-application
down-application:
	$(compose_application) down

.PHONY: destroy-application
destroy-application:
	$(compose_application) down -v

.PHONY: restart-application
restart-application:
	$(compose_application) stop
	$(compose_application) up -d

.PHONY: application-logs
application-logs:
	$(compose_application) logs -f
# ==========================================DOCKER(APP)===========================================

# ==========================================DOCKER(TESTS)=========================================
.PHONY: build-tests
build-tests:
	$(compose_tests) build

.PHONY: tests
tests:
	$(compose_tests) up $(capture_exit_code) $(exit_code_tests)

.PHONY: stop-tests
stop-tests:
	$(compose_tests) stop

.PHONY: down-tests
down-tests:
	$(compose_tests) down

.PHONY: destroy-tests
destroy-tests:
	$(compose_tests) down -v

.PHONY: restart-tests
restart-tests:
	$(compose_tests) stop
	$(compose_tests) up $(capture_exit_code) $(exit_code_tests)

.PHONY: tests-logs
tests-logs:
	$(compose_tests) logs -f
# ==========================================DOCKER(TESTS)=========================================

# ========================================DOCKER(MIGRATIONS)======================================
.PHONY: build-migrations
build-migrations:
	$(compose_migrations) build

.PHONY: migrations
migrations:
	$(compose_migrations) up $(capture_exit_code) $(exit_code_migrations)

.PHONY: stop-migrations
stop-migrations:
	$(compose_migrations) stop

.PHONY: down-migrations
down-migrations:
	$(compose_migrations) down

.PHONY: destroy-migrations
destroy-migrations:
	$(compose_migrations) down -v

.PHONY: restart-migrations
restart-migrations:
	$(compose_migrations) stop
	$(compose_migrations) up $(capture_exit_code) $(exit_code_migrations)

.PHONY: migrations-logs
migrations-logs:
	$(compose_migrations) logs -f
# ========================================DOCKER(MIGRATIONS)======================================
