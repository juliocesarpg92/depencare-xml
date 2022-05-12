# Generate tokens

### Zoho Creator {#creator}

- https://www.zoho.com/creator/help/api/v2/authorization-request.html
- Used scopes

```text
ZohoCreator.report.READ,ZohoCreator.form.CREATE,ZohoCreator.report.UPDATE,ZohoCreator.report.CREATE
```

### Zoho CRM {#crm}

- https://www.zoho.com/crm/developer/docs/api/v2/access-refresh.html
- Used scopes

```text
ZohoCRM.coql.READ,ZohoCRM.modules.READ
```

# Installation

## install python and pip

1. download python installer from internet.
2. select the option to include python inside system path (windows).
3. open a cmd and type `pip -v` and `python` to be sure are installed.

## start venv

1. open console.
1. `python -m venv <nombrevenv>`
1. `<nombrevenv>\Scripts\activate`

## configure

1. open file `main.spec`, in line 11 change `venv` for virtual environment name used above.
2. clone file `packages/adapters/configuration/config.ini.example`.
3. rename it as `config.ini`.
4. inside `client` config section
   - update `client_id` and `client_secret` (https://api-console.zoho.eu).
5. inside `sdk` config section
   - update `refresh_token` (see [Zoho CRM section above](#crm)).
   - update `base_path` with path where project is located.
6. inside `creator` config section
   - update `refresh_token` and `access_token` (see [Zoho Creator section above](#creator)).

## install requirements

```bash
pip install -r requirements.txt
```

## build script

```bash
pyinstaller main.spec
```
