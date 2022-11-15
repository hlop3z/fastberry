import Fastberry from "fastberry";
import { Chain } from "./zeus";

import Types from "./backend/types.mjs";
import Forms from "./backend/forms.mjs";
import Operations from "./backend/operations.mjs";
import returnTypes from "./backend/returnTypes.mjs";

export default function API({
	url = "http://localhost:8000/graphql",
	ignore = ["Id"],
} = {}) {
	return Fastberry({
		url: url,
		chain: Chain,
		types: Types,
		forms: Forms,
		operations: Operations,
		ignore: ignore,
		returnTypes: returnTypes,
	});
}
