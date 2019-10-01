# Suricata JSON schema project

As discussed in the brainstorming session at SURICON 2018 in Vancouver we want to have a JSON schema for every suricata release to use in automated testing environments. A schema would also allow better documentation of the eve.json format.

Reference: https://redmine.openinfosecfoundation.org/issues/2699

## Empirical Bootstrapping of EVE-JSON Schema Documentation

Five years ago, Suricata 2.0 introduced EVE-JSON as a single common data output format for alerts, metadata and other event information. Its structured syntax makes it easy to capture diverse information in much detail and to pass it to downstream tools for further analysis. However, up to now no in-depth documentation exists for EVE-JSON (regarding both extent and meaning of fields and values), partly because it is difficult to derive an comprehensive specification from static analysis of the Suricata source code. The lack of such a spec makes it difficult for tool authors to reliably consume and interpret all variations of Suricata output. We report on our effort to jump-start documentation of the EVE-JSON format produced by Suricata empirically. In particular, we present a reproducible method to derive JSON schemas (https://json-schema.org) from the results of running various Suricata versions against diverse input traffic. We also comment on the evolution of the schema as it appears de facto and show how the generated schema information can be used to enable collaborative editing of detailed EVE-JSON documentation.

## Building Docker images

```

$ docker build --no-cache --build-arg suricata_version=4.1.5 -t satta/suricata-4.1.5 .
```