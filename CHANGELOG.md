# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [v2.8.4](https://github.com/wickerdevs/instaclient/releases/tag/v2.8.4) - 2021-01-18

<small>[Compare with v2.8.3](https://github.com/wickerdevs/instaclient/compare/v2.8.3...v2.8.4)</small>

### Fixed
- Fixed graphql issues ([da18780](https://github.com/wickerdevs/instaclient/commit/da18780b98a84d8a3257b23e8e33bb96c10af556) by David Wicker).


## [v2.8.3](https://github.com/wickerdevs/instaclient/releases/tag/v2.8.3) - 2021-01-18

<small>[Compare with v2.8.2](https://github.com/wickerdevs/instaclient/compare/v2.8.2...v2.8.3)</small>

### Changed
- Changed chortcut methods for get_followers() & get_following() ([357075d](https://github.com/wickerdevs/instaclient/commit/357075d810d7418c798fa91c47f88ba6c9d5d17d) by David Wicker).


## [v2.8.2](https://github.com/wickerdevs/instaclient/releases/tag/v2.8.2) - 2021-01-18

<small>[Compare with v2.8.0](https://github.com/wickerdevs/instaclient/compare/v2.8.0...v2.8.2)</small>


## [v2.8.0](https://github.com/wickerdevs/instaclient/releases/tag/v2.8.0) - 2021-01-18

<small>[Compare with v2.8](https://github.com/wickerdevs/instaclient/compare/v2.8...v2.8.0)</small>

### Added
- Added refresh method to hashtag & comment ([70065cf](https://github.com/wickerdevs/instaclient/commit/70065cf56a56a989f8d3751c0c0b682b5d048423) by David Wicker).

### Changed
- Changed get_followers & get_following to include ability to scrape through the graphql api ([7e5860b](https://github.com/wickerdevs/instaclient/commit/7e5860b72c80cd882a9f92e4004a03fe41c06908) by David Wicker).


## [v2.8](https://github.com/wickerdevs/instaclient/releases/tag/v2.8) - 2021-01-16

<small>[Compare with v2.7.27](https://github.com/wickerdevs/instaclient/compare/v2.7.27...v2.8)</small>

### Added
- Added get_location_posts method ([f0e3f08](https://github.com/wickerdevs/instaclient/commit/f0e3f084c4bebfcf343a1fd107030aef93776144) by David Wicker).
- Added get_location() method ([cc10422](https://github.com/wickerdevs/instaclient/commit/cc104224e3717d76469b9d0863b0963b983711a8) by David Wicker).
- Added get_search_result() method ([740671e](https://github.com/wickerdevs/instaclient/commit/740671ea106ec0e2be241feb9e8acf2a99809a95) by David Wicker).
- Add client.get_following() method ([cfed3f5](https://github.com/wickerdevs/instaclient/commit/cfed3f53a227d2e4ced65c04d6ed5a66e604ac7b) by David Wicker).

### Changed
- Change hashtag definition and methods ([c3f1b77](https://github.com/wickerdevs/instaclient/commit/c3f1b7756023a295d88ac334c3fcaeff437773ca) by David Wicker).
- Changed comment.py docs and __eq__ ([3f34a77](https://github.com/wickerdevs/instaclient/commit/3f34a7774342177f2dcd08c8eaad575efcbef1e8) by David Wicker).

### Fixed
- Fixed minor issues ([8e31351](https://github.com/wickerdevs/instaclient/commit/8e31351cb9d4fd700820215ccc6400bc07e8163a) by David Wicker).


## [v2.7.27](https://github.com/wickerdevs/instaclient/releases/tag/v2.7.27) - 2021-01-10

<small>[Compare with v2.7.26](https://github.com/wickerdevs/instaclient/compare/v2.7.26...v2.7.27)</small>

### Added
- Added _nav_explore() method; fixed _login_required() decorator. ([79b57b8](https://github.com/wickerdevs/instaclient/commit/79b57b8ab55233317817975a00b776e0b7e9fac8) by David Wicker).


## [v2.7.26](https://github.com/wickerdevs/instaclient/releases/tag/v2.7.26) - 2021-01-09

<small>[Compare with v2.7.25](https://github.com/wickerdevs/instaclient/compare/v2.7.25...v2.7.26)</small>

### Changed
- Changed behaviour of _reques() method. ([3e3d9da](https://github.com/wickerdevs/instaclient/commit/3e3d9daf1cab55503f9f9518e0738a44764015bb) by David Wicker).


## [v2.7.25](https://github.com/wickerdevs/instaclient/releases/tag/v2.7.25) - 2021-01-09

<small>[Compare with v2.7.24](https://github.com/wickerdevs/instaclient/compare/v2.7.24...v2.7.25)</small>

### Changed
- Changed readme.md ([95fbf6a](https://github.com/wickerdevs/instaclient/commit/95fbf6a45e629f614907b242fb57e4ea0df55a6b) by David Wicker).
- Changed docs ([9b98452](https://github.com/wickerdevs/instaclient/commit/9b98452d23169961a25c46cb85b5034487846812) by David Wicker).
- Changed insta methods decorator ([65000ef](https://github.com/wickerdevs/instaclient/commit/65000efcde6a29e30ddfcdb41e97f3fc2b895c1b) by David Wicker).

### Fixed
- Fixed scraper.get_profile() ([be2bc65](https://github.com/wickerdevs/instaclient/commit/be2bc659917e2ee282dd4e9e095f1e48fbc74070) by David Wicker).


## [v2.7.24](https://github.com/wickerdevs/instaclient/releases/tag/v2.7.24) - 2021-01-04

<small>[Compare with v2.7.18](https://github.com/wickerdevs/instaclient/compare/v2.7.18...v2.7.24)</small>


## [v2.7.18](https://github.com/wickerdevs/instaclient/releases/tag/v2.7.18) - 2020-12-30

<small>[Compare with v2.7](https://github.com/wickerdevs/instaclient/compare/v2.7...v2.7.18)</small>


## [v2.7](https://github.com/wickerdevs/instaclient/releases/tag/v2.7) - 2020-12-22

<small>[Compare with v2.4](https://github.com/wickerdevs/instaclient/compare/v2.4...v2.7)</small>


## [v2.4](https://github.com/wickerdevs/instaclient/releases/tag/v2.4) - 2020-12-21

<small>[Compare with v2.3](https://github.com/wickerdevs/instaclient/compare/v2.3...v2.4)</small>


## [v2.3](https://github.com/wickerdevs/instaclient/releases/tag/v2.3) - 2020-12-16

<small>[Compare with v2.2.2](https://github.com/wickerdevs/instaclient/compare/v2.2.2...v2.3)</small>


## [v2.2.2](https://github.com/wickerdevs/instaclient/releases/tag/v2.2.2) - 2020-12-10

<small>[Compare with v2.1.12](https://github.com/wickerdevs/instaclient/compare/v2.1.12...v2.2.2)</small>


## [v2.1.12](https://github.com/wickerdevs/instaclient/releases/tag/v2.1.12) - 2020-12-06

<small>[Compare with v2.1.11](https://github.com/wickerdevs/instaclient/compare/v2.1.11...v2.1.12)</small>


## [v2.1.11](https://github.com/wickerdevs/instaclient/releases/tag/v2.1.11) - 2020-12-05

<small>[Compare with v2.1.10](https://github.com/wickerdevs/instaclient/compare/v2.1.10...v2.1.11)</small>


## [v2.1.10](https://github.com/wickerdevs/instaclient/releases/tag/v2.1.10) - 2020-12-05

<small>[Compare with v2.1.9](https://github.com/wickerdevs/instaclient/compare/v2.1.9...v2.1.10)</small>


## [v2.1.9](https://github.com/wickerdevs/instaclient/releases/tag/v2.1.9) - 2020-12-05

<small>[Compare with v2.1.8](https://github.com/wickerdevs/instaclient/compare/v2.1.8...v2.1.9)</small>


## [v2.1.8](https://github.com/wickerdevs/instaclient/releases/tag/v2.1.8) - 2020-12-03

<small>[Compare with v2.1.7](https://github.com/wickerdevs/instaclient/compare/v2.1.7...v2.1.8)</small>


## [v2.1.7](https://github.com/wickerdevs/instaclient/releases/tag/v2.1.7) - 2020-12-01

<small>[Compare with v2.1.6](https://github.com/wickerdevs/instaclient/compare/v2.1.6...v2.1.7)</small>


## [v2.1.6](https://github.com/wickerdevs/instaclient/releases/tag/v2.1.6) - 2020-11-30

<small>[Compare with v2.1.5](https://github.com/wickerdevs/instaclient/compare/v2.1.5...v2.1.6)</small>


## [v2.1.5](https://github.com/wickerdevs/instaclient/releases/tag/v2.1.5) - 2020-11-29

<small>[Compare with v2.1.2](https://github.com/wickerdevs/instaclient/compare/v2.1.2...v2.1.5)</small>


## [v2.1.2](https://github.com/wickerdevs/instaclient/releases/tag/v2.1.2) - 2020-11-28

<small>[Compare with v2.1.1](https://github.com/wickerdevs/instaclient/compare/v2.1.1...v2.1.2)</small>


## [v2.1.1](https://github.com/wickerdevs/instaclient/releases/tag/v2.1.1) - 2020-11-24

<small>[Compare with v2.1](https://github.com/wickerdevs/instaclient/compare/v2.1...v2.1.1)</small>


## [v2.1](https://github.com/wickerdevs/instaclient/releases/tag/v2.1) - 2020-11-22

<small>[Compare with v1.10.10](https://github.com/wickerdevs/instaclient/compare/v1.10.10...v2.1)</small>


## [v1.10.10](https://github.com/wickerdevs/instaclient/releases/tag/v1.10.10) - 2020-11-17

<small>[Compare with v1.10.9](https://github.com/wickerdevs/instaclient/compare/v1.10.9...v1.10.10)</small>


## [v1.10.9](https://github.com/wickerdevs/instaclient/releases/tag/v1.10.9) - 2020-11-17

<small>[Compare with v1.10.8](https://github.com/wickerdevs/instaclient/compare/v1.10.8...v1.10.9)</small>


## [v1.10.8](https://github.com/wickerdevs/instaclient/releases/tag/v1.10.8) - 2020-11-17

<small>[Compare with v1.10.7](https://github.com/wickerdevs/instaclient/compare/v1.10.7...v1.10.8)</small>


## [v1.10.7](https://github.com/wickerdevs/instaclient/releases/tag/v1.10.7) - 2020-11-17

<small>[Compare with v1.10.6](https://github.com/wickerdevs/instaclient/compare/v1.10.6...v1.10.7)</small>


## [v1.10.6](https://github.com/wickerdevs/instaclient/releases/tag/v1.10.6) - 2020-11-17

<small>[Compare with v1.10.5](https://github.com/wickerdevs/instaclient/compare/v1.10.5...v1.10.6)</small>


## [v1.10.5](https://github.com/wickerdevs/instaclient/releases/tag/v1.10.5) - 2020-11-17

<small>[Compare with v1.10.4](https://github.com/wickerdevs/instaclient/compare/v1.10.4...v1.10.5)</small>


## [v1.10.4](https://github.com/wickerdevs/instaclient/releases/tag/v1.10.4) - 2020-11-16

<small>[Compare with v1.10.3](https://github.com/wickerdevs/instaclient/compare/v1.10.3...v1.10.4)</small>


## [v1.10.3](https://github.com/wickerdevs/instaclient/releases/tag/v1.10.3) - 2020-11-16

<small>[Compare with v1.10.2](https://github.com/wickerdevs/instaclient/compare/v1.10.2...v1.10.3)</small>


## [v1.10.2](https://github.com/wickerdevs/instaclient/releases/tag/v1.10.2) - 2020-11-16

<small>[Compare with v1.10.1](https://github.com/wickerdevs/instaclient/compare/v1.10.1...v1.10.2)</small>


## [v1.10.1](https://github.com/wickerdevs/instaclient/releases/tag/v1.10.1) - 2020-11-15

<small>[Compare with v1.9.21](https://github.com/wickerdevs/instaclient/compare/v1.9.21...v1.10.1)</small>


## [v1.9.21](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.21) - 2020-11-13

<small>[Compare with v1.9.20](https://github.com/wickerdevs/instaclient/compare/v1.9.20...v1.9.21)</small>


## [v1.9.20](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.20) - 2020-11-11

<small>[Compare with v1.9.19](https://github.com/wickerdevs/instaclient/compare/v1.9.19...v1.9.20)</small>


## [v1.9.19](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.19) - 2020-11-11

<small>[Compare with v1.9.18](https://github.com/wickerdevs/instaclient/compare/v1.9.18...v1.9.19)</small>


## [v1.9.18](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.18) - 2020-11-09

<small>[Compare with v1.9.17](https://github.com/wickerdevs/instaclient/compare/v1.9.17...v1.9.18)</small>


## [v1.9.17](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.17) - 2020-11-08

<small>[Compare with v1.9.16](https://github.com/wickerdevs/instaclient/compare/v1.9.16...v1.9.17)</small>


## [v1.9.16](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.16) - 2020-11-08

<small>[Compare with v1.9.15](https://github.com/wickerdevs/instaclient/compare/v1.9.15...v1.9.16)</small>


## [v1.9.15](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.15) - 2020-11-08

<small>[Compare with v1.9.14](https://github.com/wickerdevs/instaclient/compare/v1.9.14...v1.9.15)</small>


## [v1.9.14](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.14) - 2020-11-08

<small>[Compare with v1.9.13](https://github.com/wickerdevs/instaclient/compare/v1.9.13...v1.9.14)</small>


## [v1.9.13](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.13) - 2020-11-08

<small>[Compare with v1.9.12](https://github.com/wickerdevs/instaclient/compare/v1.9.12...v1.9.13)</small>


## [v1.9.12](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.12) - 2020-11-08

<small>[Compare with v1.9.10](https://github.com/wickerdevs/instaclient/compare/v1.9.10...v1.9.12)</small>


## [v1.9.10](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.10) - 2020-11-08

<small>[Compare with v1.9.9](https://github.com/wickerdevs/instaclient/compare/v1.9.9...v1.9.10)</small>


## [v1.9.9](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.9) - 2020-11-08

<small>[Compare with v1.9.7](https://github.com/wickerdevs/instaclient/compare/v1.9.7...v1.9.9)</small>


## [v1.9.7](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.7) - 2020-11-07

<small>[Compare with v1.9.6](https://github.com/wickerdevs/instaclient/compare/v1.9.6...v1.9.7)</small>


## [v1.9.6](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.6) - 2020-11-07

<small>[Compare with v1.9.5](https://github.com/wickerdevs/instaclient/compare/v1.9.5...v1.9.6)</small>


## [v1.9.5](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.5) - 2020-11-07

<small>[Compare with v1.9.2](https://github.com/wickerdevs/instaclient/compare/v1.9.2...v1.9.5)</small>

### Added
- Add drivers module ([869e53a](https://github.com/wickerdevs/instaclient/commit/869e53ae4f9b3445e2c486a951ef281742321961) by David Wicker).


## [v1.9.2](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.2) - 2020-11-05

<small>[Compare with v1.9.1](https://github.com/wickerdevs/instaclient/compare/v1.9.1...v1.9.2)</small>


## [v1.9.1](https://github.com/wickerdevs/instaclient/releases/tag/v1.9.1) - 2020-11-01

<small>[Compare with v1.8.1](https://github.com/wickerdevs/instaclient/compare/v1.8.1...v1.9.1)</small>


## [v1.8.1](https://github.com/wickerdevs/instaclient/releases/tag/v1.8.1) - 2020-10-31

<small>[Compare with v1.7.6](https://github.com/wickerdevs/instaclient/compare/v1.7.6...v1.8.1)</small>


## [v1.7.6](https://github.com/wickerdevs/instaclient/releases/tag/v1.7.6) - 2020-10-29

<small>[Compare with v1.7.5](https://github.com/wickerdevs/instaclient/compare/v1.7.5...v1.7.6)</small>


## [v1.7.5](https://github.com/wickerdevs/instaclient/releases/tag/v1.7.5) - 2020-10-29

<small>[Compare with v1.7.4](https://github.com/wickerdevs/instaclient/compare/v1.7.4...v1.7.5)</small>


## [v1.7.4](https://github.com/wickerdevs/instaclient/releases/tag/v1.7.4) - 2020-10-29

<small>[Compare with v1.7.2](https://github.com/wickerdevs/instaclient/compare/v1.7.2...v1.7.4)</small>


## [v1.7.2](https://github.com/wickerdevs/instaclient/releases/tag/v1.7.2) - 2020-10-29

<small>[Compare with v1.7.1](https://github.com/wickerdevs/instaclient/compare/v1.7.1...v1.7.2)</small>


## [v1.7.1](https://github.com/wickerdevs/instaclient/releases/tag/v1.7.1) - 2020-10-29

<small>[Compare with v1.6.5](https://github.com/wickerdevs/instaclient/compare/v1.6.5...v1.7.1)</small>


## [v1.6.5](https://github.com/wickerdevs/instaclient/releases/tag/v1.6.5) - 2020-10-29

<small>[Compare with v1.6.4](https://github.com/wickerdevs/instaclient/compare/v1.6.4...v1.6.5)</small>


## [v1.6.4](https://github.com/wickerdevs/instaclient/releases/tag/v1.6.4) - 2020-10-29

<small>[Compare with v1.6.3](https://github.com/wickerdevs/instaclient/compare/v1.6.3...v1.6.4)</small>


## [v1.6.3](https://github.com/wickerdevs/instaclient/releases/tag/v1.6.3) - 2020-10-29

<small>[Compare with v1.6.2](https://github.com/wickerdevs/instaclient/compare/v1.6.2...v1.6.3)</small>


## [v1.6.2](https://github.com/wickerdevs/instaclient/releases/tag/v1.6.2) - 2020-10-28

<small>[Compare with v1.6.1](https://github.com/wickerdevs/instaclient/compare/v1.6.1...v1.6.2)</small>


## [v1.6.1](https://github.com/wickerdevs/instaclient/releases/tag/v1.6.1) - 2020-10-28

<small>[Compare with v1.5.4](https://github.com/wickerdevs/instaclient/compare/v1.5.4...v1.6.1)</small>


## [v1.5.4](https://github.com/wickerdevs/instaclient/releases/tag/v1.5.4) - 2020-10-27

<small>[Compare with v1.5.2](https://github.com/wickerdevs/instaclient/compare/v1.5.2...v1.5.4)</small>


## [v1.5.2](https://github.com/wickerdevs/instaclient/releases/tag/v1.5.2) - 2020-10-27

<small>[Compare with v1.5.1](https://github.com/wickerdevs/instaclient/compare/v1.5.1...v1.5.2)</small>


## [v1.5.1](https://github.com/wickerdevs/instaclient/releases/tag/v1.5.1) - 2020-10-27

<small>[Compare with v1.4.3](https://github.com/wickerdevs/instaclient/compare/v1.4.3...v1.5.1)</small>


## [v1.4.3](https://github.com/wickerdevs/instaclient/releases/tag/v1.4.3) - 2020-10-26

<small>[Compare with v1.4.2](https://github.com/wickerdevs/instaclient/compare/v1.4.2...v1.4.3)</small>

### Fixed
- Fixed host error ([7666513](https://github.com/wickerdevs/instaclient/commit/76665135df317762e7f79d87ebe13613eaf4bd17) by David Wicker).


## [v1.4.2](https://github.com/wickerdevs/instaclient/releases/tag/v1.4.2) - 2020-10-26

<small>[Compare with v1.4.1](https://github.com/wickerdevs/instaclient/compare/v1.4.1...v1.4.2)</small>


## [v1.4.1](https://github.com/wickerdevs/instaclient/releases/tag/v1.4.1) - 2020-10-21

<small>[Compare with v1.4](https://github.com/wickerdevs/instaclient/compare/v1.4...v1.4.1)</small>


## [v1.4](https://github.com/wickerdevs/instaclient/releases/tag/v1.4) - 2020-10-21

<small>[Compare with v1.3](https://github.com/wickerdevs/instaclient/compare/v1.3...v1.4)</small>


## [v1.3](https://github.com/wickerdevs/instaclient/releases/tag/v1.3) - 2020-10-18

<small>[Compare with v1.2](https://github.com/wickerdevs/instaclient/compare/v1.2...v1.3)</small>


## [v1.2](https://github.com/wickerdevs/instaclient/releases/tag/v1.2) - 2020-10-17

<small>[Compare with v1.1.0](https://github.com/wickerdevs/instaclient/compare/v1.1.0...v1.2)</small>


## [v1.1.0](https://github.com/wickerdevs/instaclient/releases/tag/v1.1.0) - 2020-10-17

<small>[Compare with first commit](https://github.com/wickerdevs/instaclient/compare/6cf19a5edce479e6314bbae779653ae79c61462e...v1.1.0)</small>


