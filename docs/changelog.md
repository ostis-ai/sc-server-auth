# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v0.1.0]
### Added
 - Support of PostgreSQL and SQLite;
 - Data classes of the sc-server for objects manipulating;
 - Password validation (supported hash of password);
 - Endpoint for getting refresh and access token by username and password;
 - Endpoint for getting access token by refresh token;
 - Endpoint for getting access token by Google account;
 - Endpoints for creating/deleting user;
 - Endpoint for getting users list;
 - Tests infrastructure for endpoints;
 - Code linting tools: isort, pylint, black;
 - CI-workflows for checking messages of commits, code linting and testing 
package on multiple environments and python versions;
 - Scripts for admin creating, local CI-checks and sort python imports;
 - README.md;
