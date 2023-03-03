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
    function getObj(e,t,n,r=0){const s={};return Object.keys(n).forEach((o=>{const i=n[o];if(!(r>t))if(!0===i)s[o]=i;else if(!1===i);else{const n=e.model[i];s[o]=getObj(e,t,n,r+1)}})),s}function getModel(e,t,n=2){return getObj(e,n,t)}function getForms(e,t,n,r){const s={};return r.forEach((r=>{const o=e[t][r][n],i="{}"===JSON.stringify(o)||"[]"===JSON.stringify(o);s[r]=i?null:Object.freeze(o)})),Object.freeze(s)}function getModels(e,t){const n={};return t.forEach((t=>{const r=e[t].model;n[t]=r||!0})),Object.freeze(n)}function createApiChain(e,t,n,r){const s={};return s[n]=[r.model,r.form],e.chain(t,s)}function setValueByPath(e,t,n){let r=e;return function e(t,n,r){let s=n.shift();t.hasOwnProperty(s)&&(0===n.length?t[s]=r:e(t[s],n,r))}(r,t.split("."),n),r}function getGraphqlSetup(e,t,n,r){const s={...e.form[t][n]},o=e.returnType[t][n];let i=null;if(o)if(1===o.length){const t=o[0];let n=e.model(t);n=JSON.parse(JSON.stringify(n)),r&&r.forEach((e=>{n=setValueByPath(n,e,!1)})),i=n}else o.length>1&&(i={},o.forEach((t=>{const n=`...on ${t}`;let s=e.model(t);s=JSON.parse(JSON.stringify(s)),r&&r[t]&&r[t].forEach((e=>{s=setValueByPath(s,e,!1)})),i[n]=s})));return{form:s,model:i,run:r=>createApiChain(e.chain,t,n,r)}}class ClientGQL{constructor(e,t=4,n){this.chain=n,this._schema=Object.freeze(e),this._maxDepth=t,this._keys={query:Object.keys(e.query),mutation:Object.keys(e.mutation),model:Object.keys(e.model)},this._forms={query:getForms(e,"query","form",this.keys.query),mutation:getForms(e,"mutation","form",this.keys.mutation)},this._args={query:getForms(e,"query","args",this.keys.query),mutation:getForms(e,"mutation","args",this.keys.mutation)},this._returnType={query:getModels(e.query,this.keys.query),mutation:getModels(e.mutation,this.keys.mutation)}}get dir(){return["schema","keys","create","form","args","returnType"]}get schema(){return this._schema}get keys(){return this._keys}get form(){return this._forms}get args(){return this._args}get returnType(){return this._returnType}create(e,t,n=null){return getGraphqlSetup(this,e,t,n)}model(e,t=null){const n=t||this._maxDepth;return getModel(this.schema,this.schema.model[e],n)}}function createGraphQLRequest(e,t){function n(e){return JSON.stringify(function(e){return"number"==typeof e?e:parseFloat(e)||parseInt(e)||e}(e))}function r(e,t,r){let s=`${function(e){if("object"==typeof e){const t=Object.keys(e)[0];return t+" : "+e[t]}return e}(e)}`;return s+=function(e={}){let t="";if(e&&Object.keys(e).length>0){t+="(";const r=[];Object.keys(e).forEach((t=>{const s=[];let o=e[t];o instanceof Object?(Object.keys(o).forEach((e=>{s.push(`${e}: ${n(o[e])}`)})),r.push(`${t}: { ${s} }`)):r.push(`${t}: ${n(o)}`)})),t+=r.join(", "),t+=")"}return t}(r),s+=" "+function(e){let t="{";return function e(n,r){Object.keys(n).forEach((r=>{"object"==typeof n[r]?(t+=` ${r} {`,e(n[r],r),t+=" }"):n[r]&&(t+=` ${r}`)}))}(e),t+=" }",t}(t),s}let s=`${e} { `;return Object.keys(t).forEach((e=>{const n=t[e],o=r(e,n[0],n[1]);s+=" ",s+=o})),s+=" }",s.trim()}function APIHandler(e,t){return new Promise(((n,r)=>{fetch(e,t).then((e=>e.json())).then((e=>n(e))).catch((e=>r(e)))}))}class API{constructor(e,t,n){this._debug=null!==n&&n,this._host=e,this._options=t}post(e=!1){const t={method:"POST"};e&&(t.body=JSON.stringify(e));const n={...this._options,...t};return APIHandler(this._host,n)}graphql(e=null){return this.post({query:e})}async chain(e,t){const n=createGraphQLRequest(e,t),{data:r,errors:s}=await this.graphql(n);return this._debug&&s&&console.error(s),r}}function createAPI(e,t={},n=null){return new API(e,{mode:"cors",credentials:"same-origin",headers:{Accept:"application/json","Content-Type":"application/json; charset=UTF-8"},...t},n)}function GraphQL(e,t,n,r){return new ClientGQL({...t,model:n},r,e)}function isBlank(e,t=null){return e||t}function Api(e){let t=null,n=null;const r=null!=e.debug&&e.debug,s=isBlank(e.maxDepth,4);return t=createAPI(e.url,e.config,r),e.schema&&e.models&&(n=GraphQL(t,e.schema,e.models,s)),{admin:n,chain:(...e)=>t.chain(...e),gql:(...e)=>n.create(...e)}}export default function Wrap(e){return"object"==typeof e?Api({schema:schema,models:models,...e}):createAPI(e)}
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
