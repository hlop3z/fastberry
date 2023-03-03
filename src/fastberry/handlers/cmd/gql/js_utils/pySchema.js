function getObj(schema, maxDepth, obj, currentDepth = 0) {
  const returnValue = {};
  Object.keys(obj).forEach((key) => {
    const current = obj[key];
    if (currentDepth > maxDepth) {
      return;
    }
    if (current === true) {
      returnValue[key] = current;
    } else if (current === false) {
      //pass
    } else {
      const childObj = schema.model[current];
      returnValue[key] = getObj(schema, maxDepth, childObj, currentDepth + 1);
    }
  });
  return returnValue;
}

function getModel(schema, obj, maxDepth = 2) {
  return getObj(schema, maxDepth, obj);
}

function getForms(schema, opType, opPart, ops) {
  const queryForms = {};
  ops.forEach((key) => {
    const currentForm = schema[opType][key][opPart];
    const isEmpty =
      JSON.stringify(currentForm) === "{}" ||
      JSON.stringify(currentForm) === "[]";
    if (!isEmpty) {
      queryForms[key] = Object.freeze(currentForm);
    } else {
      queryForms[key] = null;
    }
  });
  return Object.freeze(queryForms);
}

function getModels(items, keys) {
  const models = {};
  keys.forEach((key) => {
    const current = items[key].model;
    models[key] = !current ? true : current;
  });
  return Object.freeze(models);
}

function createApiChain(chainAdmin, opType, opName, instance) {
  const request = {};
  request[opName] = [instance.model, instance.form];
  return chainAdmin.chain(opType, request);
}

function setValueByPath(obj, path, value) {
  let pathArray = path.split(".");
  let current = obj;

  function setValue(obj, pathArray, value) {
    let key = pathArray.shift();
    if (!obj.hasOwnProperty(key)) {
      return;
    }
    if (pathArray.length === 0) {
      obj[key] = value;
    } else {
      setValue(obj[key], pathArray, value);
    }
  }
  setValue(current, pathArray, value);
  return current;
}

function getGraphqlSetup(admin, opType, name, disable) {
  const form = { ...admin.form[opType][name] };
  const models = admin.returnType[opType][name];
  let model = null;
  if (models) {
    if (models.length === 1) {
      const element = models[0];
      let config = admin.model(element);
      config = JSON.parse(JSON.stringify(config));
      if (disable) {
        disable.forEach((key) => {
          config = setValueByPath(config, key, false);
        });
      }
      model = config;
    } else if (models.length > 1) {
      model = {};
      models.forEach((element) => {
        const queryKey = `...on ${element}`;
        let config = admin.model(element);
        config = JSON.parse(JSON.stringify(config));
        if (disable) {
          if (disable[element]) {
            disable[element].forEach((key) => {
              config = setValueByPath(config, key, false);
            });
          }
        }
        model[queryKey] = config;
      });
    }
  }

  const run = (instance) => createApiChain(admin.chain, opType, name, instance);

  return {
    form,
    model,
    run,
  };
}

class ClientGQL {
  constructor(schema, maxDepth = 4, chain) {
    this.chain = chain;
    this._schema = Object.freeze(schema);
    this._maxDepth = maxDepth;
    this._keys = {
      query: Object.keys(schema["query"]),
      mutation: Object.keys(schema["mutation"]),
      model: Object.keys(schema["model"]),
    };
    this._forms = {
      query: getForms(schema, "query", "form", this.keys.query),
      mutation: getForms(schema, "mutation", "form", this.keys.mutation),
    };
    this._args = {
      query: getForms(schema, "query", "args", this.keys.query),
      mutation: getForms(schema, "mutation", "args", this.keys.mutation),
    };
    this._returnType = {
      query: getModels(schema["query"], this.keys.query),
      mutation: getModels(schema["mutation"], this.keys.mutation),
    };
  }
  get dir() {
    return ["schema", "keys", "create", "form", "args", "returnType"];
  }
  get schema() {
    return this._schema;
  }
  get keys() {
    return this._keys;
  }
  get form() {
    return this._forms;
  }
  get args() {
    return this._args;
  }
  get returnType() {
    return this._returnType;
  }

  create(opType, name, disable = null) {
    return getGraphqlSetup(this, opType, name, disable);
  }
  model(name, maxDepth = null) {
    const _maxDepth = maxDepth ? maxDepth : this._maxDepth;
    return getModel(this.schema, this.schema.model[name], _maxDepth);
  }
}

// Dynamic Requests
function createGraphQLRequest(opType, reqObj) {
  function parseNumber(value) {
    if (typeof value === "number") {
      return value;
    } else {
      return parseFloat(value) || parseInt(value) || value;
    }
  }
  function parseValue(value) {
    return JSON.stringify(parseNumber(value));
  }
  function createGraphQLFields(obj) {
    let query = "{";
    function buildQuery(obj, parent) {
      Object.keys(obj).forEach((key) => {
        if (typeof obj[key] === "object") {
          query += ` ${key} {`;
          buildQuery(obj[key], key);
          query += ` }`;
        } else if (obj[key]) {
          query += ` ${key}`;
        }
      });
    }
    buildQuery(obj);
    query += " }";
    return query;
  }
  function createGraphQLArgs(inputArgs = {}) {
    let operationString = "";
    if (inputArgs && Object.keys(inputArgs).length > 0) {
      operationString += "(";
      const items = [];
      Object.keys(inputArgs).forEach((arg) => {
        const childItems = [];
        let theArgs = inputArgs[arg];
        if (theArgs instanceof Object) {
          Object.keys(theArgs).forEach((key) => {
            childItems.push(`${key}: ${parseValue(theArgs[key])}`);
          });
          items.push(`${arg}: { ${childItems} }`);
        } else {
          items.push(`${arg}: ${parseValue(theArgs)}`);
        }
      });
      operationString += items.join(", ");
      operationString += ")";
    }
    return operationString;
  }

  function createOperationName(value) {
    if (typeof value === "object") {
      const key = Object.keys(value)[0];
      return key + " : " + value[key];
    } else {
      return value;
    }
  }
  function createGraphQLOperation(operationName, fields, inputArgs) {
    let operationString = `${createOperationName(operationName)}`;
    // Handle Args
    operationString += createGraphQLArgs(inputArgs);
    // Handle Fields
    operationString += " " + createGraphQLFields(fields);
    return operationString;
  }

  let operationString = `${opType} { `;

  // Build GraphQL Request Object
  Object.keys(reqObj).forEach((key) => {
    const current = reqObj[key];
    const gqlQuery = createGraphQLOperation(key, current[0], current[1]);
    operationString += " ";
    operationString += gqlQuery;
  });

  operationString += " }";
  return operationString.trim();
}

// API - Handler
function APIHandler(URL, OPTIONS) {
  return new Promise((myResolve, myReject) => {
    fetch(URL, OPTIONS)
      .then((response) => response.json())
      .then((json) => myResolve(json))
      .catch((error) => myReject(error));
  });
}

class API {
  constructor(baseURL, options, debug) {
    this._debug = debug === null ? false : debug;
    this._host = baseURL;
    this._options = options;
  }
  /* POST */
  ["post"](data = false) {
    const request = { method: "POST" };
    if (data) {
      request.body = JSON.stringify(data);
    }
    const options = { ...this._options, ...request };
    return APIHandler(this._host, options);
  }
  /* GraphQL */
  ["graphql"](query = null) {
    return this.post({ query: query });
  }
  /* Chain */
  async ["chain"](opType, request) {
    const codeText = createGraphQLRequest(opType, request);
    const { data, errors } = await this.graphql(codeText);
    if (this._debug && errors) {
      console.error(errors);
    }
    return data;
  }
}

/* Create - API */
function createAPI(baseURL, options = {}, debug = null) {
  const OPTIONS = {
    mode: "cors",
    credentials: "same-origin", // same-origin include
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json; charset=UTF-8",
    },
  };
  return new API(baseURL, { ...OPTIONS, ...options }, debug);
}

// Wrap
function GraphQL(chain, schema, model, maxDepth) {
  return new ClientGQL({ ...schema, model: model }, maxDepth, chain);
}

function isBlank(value, state = null) {
  if (value) {
    return value;
  } else {
    return state;
  }
}

/* Allow Easy Creation */
function Api(obj) {
  let gqlAdmin = null;
  let schemaAdmin = null;

  const debug = obj.debug == undefined ? false : obj.debug;
  const maxDepth = isBlank(obj.maxDepth, 4);

  // API
  gqlAdmin = createAPI(obj.url, obj.config, debug);

  // Manager
  if (obj.schema && obj.models) {
    schemaAdmin = GraphQL(gqlAdmin, obj.schema, obj.models, maxDepth);
  }

  return {
    admin: schemaAdmin,
    chain: (...args) => gqlAdmin.chain(...args),
    gql: (...args) => schemaAdmin.create(...args),
  };
}

export default function Wrap(obj) {
  if (typeof obj === "object") {
    return Api({
      schema: schema,
      models: models,
      ...obj,
    });
  } else {
    return createAPI(obj);
  }
}
