# -*- coding: utf-8 -*-
"""
    Custom - Command-Line-Group
"""
import os
from pathlib import Path

import fastberry as fb

from .utils import Frontend, write_file

JS_README = """
# FastBerry (ESM)

## Init the **API**

```js
import client from "./client";

const api = client({
  url: "http://localhost:8000/graphql",
  debug: true,
  maxDepth: 6,
  config: {
    mode: "cors",
    credentials: "same-origin", // same-origin include
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json; charset=UTF-8",
    },
  },
});

// Pre-Built { Query(s) & Mutation(s) } from { Schema }
console.log(api.admin.keys);
```

---

## How To **Disable Fields**

```js
// Single Model
const instance = api.gql("query", "MyQuery", ["Id"]);

// Edge Model
const instance = api.gql("query", "MyQuery", ["edges.node.Id"]); // Recursive Disable ["via.dots"]

// Multi Model
const instance = api.gql("mutation", "MyMutation", { Model: ["Id"] });
```

---

## **GQL** Request Demo

```js
// Init (Editable) Instance
const instance = api.gql("query", "MyQuery", ["Id"]);

// Edit
instance.form.item = "MTo6YTU1ZTUzMmVhYjAyOGI0Mg==";

// Run
const { MyQuery } = await instance.run(instance);

console.log(MyQuery);
```

---

## **Chain** Request Demo

```js
const request = {
  MyQuery: [
    // Response
    {
      id: true,
      name: true,
    },
    // Inputs
    {
      item: "MTo6YTU1ZTUzMmVhYjAyOGI0Mg==",
    },
  ],
};

api.chain("query", request).then((response) => {
  console.log(response);
});
```
"""

# Create <Commands> here.
def build_client(schema):
    """Demo CLI Function"""

    # "Generates" Folder
    root_folder = fb.config["spoc"]["spoc"]["generates"]

    # GQL Folder
    root_folder = Path(root_folder)
    folder = root_folder / "client"

    # Schema
    frontend = Frontend(schema)

    # Main JS
    main_js = """import models from "./models";\n\n"""
    main_js += f"const schema = {frontend.schema}\n\n"
    main_js += """
    function getObj(t,e,n,r=0){const s={};return Object.keys(n).forEach((o=>{const i=n[o];if(!(r>e))if(!0===i)s[o]=i;else{const n=t.model[i];s[o]=getObj(t,e,n,r+1)}})),s}function getModel(t,e,n=2){return getObj(t,n,e)}function getForms(t,e,n,r){const s={};return r.forEach((r=>{const o=t[e][r][n],i="{}"===JSON.stringify(o)||"[]"===JSON.stringify(o);s[r]=i?null:Object.freeze(o)})),Object.freeze(s)}function getModels(t,e){const n={};return e.forEach((e=>{const r=t[e].model;n[e]=r||!0})),Object.freeze(n)}function createApiChain(t,e,n,r){const s={};return s[n]=[r.model,r.form],t.chain(e,s)}function setValueByPath(t,e,n){let r=t;return function t(e,n,r){let s=n.shift();e.hasOwnProperty(s)&&(0===n.length?e[s]=r:t(e[s],n,r))}(r,e.split("."),n),r}function getGraphqlSetup(t,e,n,r){const s={...t.form[e][n]},o=t.returnType[e][n];let i=null;if(o)if(1===o.length){const e=o[0];let n=t.model(e);n=JSON.parse(JSON.stringify(n)),r&&r.forEach((t=>{n=setValueByPath(n,t,!1)})),i=n}else o.length>1&&(i={},o.forEach((e=>{const n=`...on ${e}`;let s=t.model(e);s=JSON.parse(JSON.stringify(s)),r&&r[e]&&r[e].forEach((t=>{s=setValueByPath(s,t,!1)})),i[n]=s})));return{form:s,model:i,run:r=>createApiChain(t.chain,e,n,r)}}class ClientGQL{constructor(t,e=4,n){this.chain=n,this._schema=Object.freeze(t),this._maxDepth=e,this._keys={query:Object.keys(t.query),mutation:Object.keys(t.mutation),model:Object.keys(t.model)},this._forms={query:getForms(t,"query","form",this.keys.query),mutation:getForms(t,"mutation","form",this.keys.mutation)},this._args={query:getForms(t,"query","args",this.keys.query),mutation:getForms(t,"mutation","args",this.keys.mutation)},this._returnType={query:getModels(t.query,this.keys.query),mutation:getModels(t.mutation,this.keys.mutation)}}get dir(){return["schema","keys","create","form","args","returnType"]}get schema(){return this._schema}get keys(){return this._keys}get form(){return this._forms}get args(){return this._args}get returnType(){return this._returnType}create(t,e,n=null){return getGraphqlSetup(this,t,e,n)}model(t,e=null){const n=e||this._maxDepth;return getModel(this.schema,this.schema.model[t],n)}}function createGraphQLRequest(t,e){function n(t){return JSON.stringify(function(t){return"number"==typeof t?t:parseFloat(t)||parseInt(t)||t}(t))}function r(t,e,r){let s=`${function(t){if("object"==typeof t){const e=Object.keys(t)[0];return e+" : "+t[e]}return t}(t)}`;return s+=function(t){let e="";if(t){e+="(";const r=[],s=[];Object.keys(t).forEach((e=>{let o=t[e];o instanceof Object?(Object.keys(o).forEach((t=>{s.push(`${t}: ${n(o[t])}`)})),r.push(`${e}: { ${s} }`)):r.push(`${e}: ${n(o)}`)})),e+=r.join(", "),e+=")"}return e}(r),s+=" "+function(t){let e="{";return function t(n,r){Object.keys(n).forEach((r=>{"object"==typeof n[r]?(e+=` ${r} {`,t(n[r],r),e+=" }"):n[r]&&(e+=` ${r}`)}))}(t),e+=" }",e}(e),s}let s=`${t} { `;return Object.keys(e).forEach((t=>{const n=e[t],o=r(t,n[0],n[1]);s+=" ",s+=o})),s+=" }",s.trim()}function APIHandler(t,e){return new Promise(((n,r)=>{fetch(t,e).then((t=>t.json())).then((t=>n(t))).catch((t=>r(t)))}))}class API{constructor(t,e,n){this._debug=null!==n&&n,this._host=t,this._options=e}post(t=!1){const e={method:"POST"};t&&(e.body=JSON.stringify(t));const n={...this._options,...e};return APIHandler(this._host,n)}graphql(t=null){return this.post({query:t})}async chain(t,e){const n=createGraphQLRequest(t,e),{data:r,errors:s}=await this.graphql(n);return this._debug&&s&&console.error(s),r}}function createAPI(t,e={},n=null){return new API(t,{mode:"cors",credentials:"same-origin",headers:{Accept:"application/json","Content-Type":"application/json; charset=UTF-8"},...e},n)}function GraphQL(t,e,n,r){return new ClientGQL({...e,model:n},r,t)}function isBlank(t,e=null){return t||e}function Api(t){let e=null,n=null;const r=null!=t.debug&&t.debug,s=isBlank(t.maxDepth,4);return e=createAPI(t.url,t.config,r),t.schema&&t.models&&(n=GraphQL(e,t.schema,t.models,s)),{admin:n,chain:(...t)=>e.chain(...t),gql:(...t)=>n.create(...t)}}export default function Wrap(t){return"object"==typeof t?Api({schema:schema,models:models,...t}):createAPI(t)}
    """.strip()

    # Schema
    # write_file(root_folder / "schema.graphql", str(schema))

    # README
    write_file(root_folder / "README.md", JS_README)

    # INDEX
    write_file(folder / "index.js", main_js)

    # Models
    write_file(folder / "models.js", f"export default {frontend.models}")

    # Run Build
    os.chdir(folder)
