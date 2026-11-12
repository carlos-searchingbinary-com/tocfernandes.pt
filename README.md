# tocfernandes.pt

Site da CJF – Contabilidades Jorge Fernandes. Página estática (`index.html`, sem build), publicada com GitHub Pages.

## Domínio

DNS (Amen) para `tocfernandes.pt`:

| Registo | Tipo | Valor |
|---|---|---|
| `@` | A | 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 |
| `www` | CNAME | `carlos-searchingbinary-com.github.io` |

Não mexer nos registos MX/TXT (email Office 365) nem em `server`.

Depois de o DNS propagar: *Settings → Pages → Custom domain* = `tocfernandes.pt`, e ativar *Enforce HTTPS* (o certificado é emitido automaticamente pelo GitHub).

## Línguas

As páginas na raiz (português) são a fonte. As versões `en/`, `es/` e `fr/` são geradas:

    python3 _build.py

As traduções estão em `_i18n.py`. O script falha se alguma frase em português não tiver tradução, por isso corre-o sempre que alterares uma página e faz commit do resultado.
