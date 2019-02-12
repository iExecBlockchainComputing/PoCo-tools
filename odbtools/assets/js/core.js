var $                 = require('jquery');
var Web3              = require('web3')
var bootstrap         = require('bootstrap')

/*****************************************************************************
 *                                Environment                                *
 *****************************************************************************/

var AppABI         = null;
var DatasetABI     = null;
var WorkerpoolABI  = null;
var IexecClerk     = null;
var IexecHub       = null;
var RLC            = null;

const NULLDATASET = {"dataset":"0x0000000000000000000000000000000000000000","datasetprice":0,"volume":0,"tag":"0x0000000000000000000000000000000000000000000000000000000000000000","apprestrict":"0x0000000000000000000000000000000000000000","workerpoolrestrict":"0x0000000000000000000000000000000000000000","requesterrestrict":"0x0000000000000000000000000000000000000000","salt":"0x0000000000000000000000000000000000000000","sign":{"r":"0x0000000000000000000000000000000000000000000000000000000000000000","s":"0x0000000000000000000000000000000000000000000000000000000000000000","v":0}};

var DOMAIN =
{
	name:              "iExecODB",
	version:           "3.0-alpha",
	chainId:           null,
	verifyingContract: null,
};

var TYPES =
{
	EIP712Domain: [
		{ name: "name",              type: "string"  },
		{ name: "version",           type: "string"  },
		{ name: "chainId",           type: "uint256" },
		{ name: "verifyingContract", type: "address" },
	],
	AppOrder: [
		{ name: "app",                type: "address" },
		{ name: "appprice",           type: "uint256" },
		{ name: "volume",             type: "uint256" },
		{ name: "tag",                type: "bytes32" },
		{ name: "datasetrestrict",    type: "address" },
		{ name: "workerpoolrestrict", type: "address" },
		{ name: "requesterrestrict",  type: "address" },
		{ name: "salt",               type: "bytes32" },
	],
	DatasetOrder: [
		{ name: "dataset",            type: "address" },
		{ name: "datasetprice",       type: "uint256" },
		{ name: "volume",             type: "uint256" },
		{ name: "tag",                type: "bytes32" },
		{ name: "apprestrict",        type: "address" },
		{ name: "workerpoolrestrict", type: "address" },
		{ name: "requesterrestrict",  type: "address" },
		{ name: "salt",               type: "bytes32" },
	],
	WorkerpoolOrder: [
		{ name: "workerpool",        type: "address" },
		{ name: "workerpoolprice",   type: "uint256" },
		{ name: "volume",            type: "uint256" },
		{ name: "tag",               type: "bytes32" },
		{ name: "category",          type: "uint256" },
		{ name: "trust",             type: "uint256" },
		{ name: "apprestrict",       type: "address" },
		{ name: "datasetrestrict",   type: "address" },
		{ name: "requesterrestrict", type: "address" },
		{ name: "salt",              type: "bytes32" },
	],
	RequestOrder: [
		{ name: "app",                type: "address" },
		{ name: "appmaxprice",        type: "uint256" },
		{ name: "dataset",            type: "address" },
		{ name: "datasetmaxprice",    type: "uint256" },
		{ name: "workerpool",         type: "address" },
		{ name: "workerpoolmaxprice", type: "uint256" },
		{ name: "requester",          type: "address" },
		{ name: "volume",             type: "uint256" },
		{ name: "tag",                type: "bytes32" },
		{ name: "category",           type: "uint256" },
		{ name: "trust",              type: "uint256" },
		{ name: "beneficiary",        type: "address" },
		{ name: "callback",           type: "address" },
		{ name: "params",             type: "string"  },
		{ name: "salt",               type: "bytes32" },
	],
};

/*****************************************************************************
 *                                  Methods                                  *
 *****************************************************************************/

function typeHash(type)
{
	return web3.utils.keccak256(type + "(" + TYPES[type].map(o => o.type + " " + o.name).join(',') + ")");
}

function AppOrderStructHash(apporder)
{
	return web3.utils.keccak256(web3.eth.abi.encodeParameters([
		"bytes32",
		"address",
		"uint256",
		"uint256",
		"bytes32",
		"address",
		"address",
		"address",
		"bytes32",
	],[
		typeHash("AppOrder"),
		apporder.app,
		apporder.appprice,
		apporder.volume,
		apporder.tag,
		apporder.datasetrestrict,
		apporder.workerpoolrestrict,
		apporder.requesterrestrict,
		apporder.salt,
	]));
}

function DatasetOrderStructHash(datasetorder)
{
	return web3.utils.keccak256(web3.eth.abi.encodeParameters([
		"bytes32",
		"address",
		"uint256",
		"uint256",
		"bytes32",
		"address",
		"address",
		"address",
		"bytes32",
	],[
		typeHash("DatasetOrder"),
		datasetorder.dataset,
		datasetorder.datasetprice,
		datasetorder.volume,
		datasetorder.tag,
		datasetorder.apprestrict,
		datasetorder.workerpoolrestrict,
		datasetorder.requesterrestrict,
		datasetorder.salt,
	]));
}

function WorkerpoolOrderStructHash(workerpoolorder)
{
	return web3.utils.keccak256(web3.eth.abi.encodeParameters([
		"bytes32",
		"address",
		"uint256",
		"uint256",
		"bytes32",
		"uint256",
		"uint256",
		"address",
		"address",
		"address",
		"bytes32",
	],[
		typeHash("WorkerpoolOrder"),
		workerpoolorder.workerpool,
		workerpoolorder.workerpoolprice,
		workerpoolorder.volume,
		workerpoolorder.tag,
		workerpoolorder.category,
		workerpoolorder.trust,
		workerpoolorder.apprestrict,
		workerpoolorder.datasetrestrict,
		workerpoolorder.requesterrestrict,
		workerpoolorder.salt,
	]));
}

function RequestOrderStructHash(requestorder)
{
	return web3.utils.keccak256(web3.eth.abi.encodeParameters([
		"bytes32",
		"address",
		"uint256",
		"address",
		"uint256",
		"address",
		"uint256",
		"address",
		"uint256",
		"bytes32",
		"uint256",
		"uint256",
		"address",
		"address",
		"bytes32",
		"bytes32",
	],[
		typeHash("RequestOrder"),
		requestorder.app,
		requestorder.appmaxprice,
		requestorder.dataset,
		requestorder.datasetmaxprice,
		requestorder.workerpool,
		requestorder.workerpoolmaxprice,
		requestorder.requester,
		requestorder.volume,
		requestorder.tag,
		requestorder.category,
		requestorder.trust,
		requestorder.beneficiary,
		requestorder.callback,
		web3.utils.keccak256(requestorder.params),
		requestorder.salt,
	]));
}

function isValidOrder(type, order)
{
	return TYPES[type].every(v => order[v.name] !== undefined);
}

function getOrderOwner(order)
{
	return new Promise((resolve, reject) => {
		if (isValidOrder("AppOrder", order))
		{
			(new web3.eth.Contract(AppABI, order.app)).methods.m_owner().call().then(resolve);
		}
		else if (isValidOrder("DatasetOrder", order))
		{
			(new web3.eth.Contract(DatasetABI, order.dataset)).methods.m_owner().call().then(resolve);
		}
		else if (isValidOrder("WorkerpoolOrder", order))
		{
			(new web3.eth.Contract(WorkerpoolABI, order.workerpool)).methods.m_owner().call().then(resolve);
		}
		else if (isValidOrder("RequestOrder", order))
		{
			resolve(order.requester);
		}
		else
		{
			reject("Invalid order");
		}
	});
}

function signStruct(typename, message, wallet)
{
	return new Promise((resolve, reject) => {
		web3.currentProvider.sendAsync({
			method: "eth_signTypedData_v3",
			params: [ wallet, JSON.stringify({ types: TYPES, domain: DOMAIN, primaryType: typename, message: message }) ],
			from: wallet,
		}, (err, result) => {
			if (result.error == undefined)
			{
				const r = "0x" + result.result.substring(2, 66);
				const s = "0x" + result.result.substring(66, 130);
				const v = parseInt(result.result.substring(130, 132), 16);
				message.sign = { r: r, s: s, v: v };
				resolve(message);
			}
			else
			{
				reject(result);
			}
		});
	});
}

function randomHex(bytes) { return "0x"+[...Array(bytes)].map(i=>(~~(Math.random()*16)).toString(16)).join(""); }

function checkNotify() { if (Notification.permission !== "granted" && Notification.permission !== 'denied') { Notification.requestPermission(permission => { if(!('permission' in Notification)) { Notification.permission = permission; } }); } return Notification.permission === "granted"; }
function notify(content) { if (checkNotify()) { new Notification(content); } }


/*****************************************************************************
 *                                   Core                                    *
 *****************************************************************************/

async function main()
{
	if (window.ethereum)
	{
		web3 = new Web3(ethereum);
		try
		{
			await ethereum.enable();
		}
		catch (error)
		{
			console.error("Access denied by user");
			return;
		}
	}
	else if (window.web3)
	{
		web3 = new Web3(window.web3.currentProvider);
	}
	else
	{
		web3 = new Web3(new PortisProvider(portisConfig));
	}
	try
	{
		urlParams = new URLSearchParams(window.location.search);
		DOMAIN.chainId           = await web3.eth.net.getId();
		DOMAIN.verifyingContract = web3.utils.isAddress(urlParams.get("clerk")) ? urlParams.get("clerk") : "0x8BE59dA9Bf70e75Aa56bF29A3e55d22e882F91bA";

		AppABI            = (await $.getJSON("contracts/App.json"           )).abi;
		DatasetABI        = (await $.getJSON("contracts/Dataset.json"       )).abi;
		WorkerpoolABI     = (await $.getJSON("contracts/Workerpool.json"    )).abi;
		RLCABI            = (await $.getJSON("contracts/RLC.json"           )).abi;
		IexecClerkABI     = (await $.getJSON("contracts/IexecClerk.json"    )).abi;
		IexecHubABI       = (await $.getJSON("contracts/IexecHub.json"      )).abi;

		IexecClerk = new web3.eth.Contract(IexecClerkABI, DOMAIN.verifyingContract);
		IexecHub   = new web3.eth.Contract(IexecHubABI,   await IexecClerk.methods.iexechub().call());
		RLC        = new web3.eth.Contract(RLCABI,        await IexecClerk.methods.token().call());

		console.log("using web3:",  web3.version);
		console.log("using clerk:", IexecClerk._address);
		console.log("using hub:  ",   IexecHub._address);
		console.log("-- let's dance! --");
	}
	catch (e)
	{
		console.error("Exceptions raised during initialization, are contract deployed on the targeted blockchain?", e);
	}
}

main();

/*****************************************************************************
 *                                   Setup                                   *
 *****************************************************************************/

$("#apporder-advanced-view").hide();
$("#datasetorder-advanced-view").hide();
$("#workerpoolorder-advanced-view").hide();
$("#requestorder-advanced-view").hide();
$("#apporder-advanced-view-toggle").click(ev => $("#apporder-advanced-view").slideToggle());
$("#datasetorder-advanced-view-toggle").click(ev => $("#datasetorder-advanced-view").slideToggle());
$("#workerpoolorder-advanced-view-toggle").click(ev => $("#workerpoolorder-advanced-view").slideToggle());
$("#requestorder-advanced-view-toggle").click(ev => $("#requestorder-advanced-view").slideToggle());

$("#requestorder-dataset-view").hide();
$("#requestorder-dataset-view-toggle").click(ev => {
	$("#requestorder-dataset-view-toggle").parent().hide();
	$("#requestorder-dataset-view").slideToggle();
});

$("#match-datasetorder").parent().hide()
$("#match-adddataset").click(() => {
	$("#match-adddataset").parent().hide();
	$("#match-datasetorder").parent().show();
});

$("#view-progress").hide();

$("#apporder-salt-random").click(() => $("#apporder-salt").val(randomHex(32)))
$("#datasetorder-salt-random").click(() => $("#datasetorder-salt").val(randomHex(32)))
$("#workerpoolorder-salt-random").click(() => $("#workerpoolorder-salt").val(randomHex(32)))
$("#requestorder-salt-random").click(() => $("#requestorder-salt").val(randomHex(32)))

// Address modal configuration
$("#addressModal").on("show.bs.modal", event => $("#addressModal-location").val($(event.relatedTarget).data("location")));
$("#addressModal-submit").click(() => $($("#addressModal-location").val()).val($("#addressModal-value").val()));

$("#addRLC").click(() => {
	web3.currentProvider.sendAsync({
		method: "metamask_watchAsset",
		params: {
			"type": "ERC20",
			"options": {
				"address": RLC._address,
				"symbol": "RLC",
				"decimals": 9,
				"image": "http://127.0.0.1/odbtools/assets/imgs/rlc.png",
			},
		},
	}, console.log);
});

async function RequestOrderProgress(hash, volume)
{
	$("#view-progress").show();

	$("#view-progress [data-toggle=popover]").popover('dispose');
	$("#view-progress [data-toggle=popover]").remove();

	var first = 0;
	var last  = 0;

	deals = {};
	tasks = {};

	for (var idx = 0; idx < volume;)
	{
		var dealid = web3.utils.soliditySha3({ type: "bytes32", value: hash }, { type: "uint256", value: idx });
		var deal   = await IexecClerk.methods.viewDeal(dealid).call();
		if (deal.botSize == 0) break;
		deals[idx] = deal;

		var deadline = new Date((parseInt(deal.startTime) + 10 * (await IexecHub.methods.viewCategory(deal.category).call()).workClockTimeRef) * 1000);
		var finished = deadline <  Date.now();

		first     = parseInt(deal.botFirst);
		last      = first + parseInt(deal.botSize);
		var style = finished ? "bg-info" : "bg-success";
		var width = (parseInt(deal.botSize)*100/volume) + "%";
		var title = "Deal " + dealid;

		var descr = [];
		descr.push("Tasks " + (first+1) + " → " + last);
		descr.push("Pool: " + deal.workerpool.pointer);
		descr.push("Category: " + deal.category);
		descr.push("Trust: " + deal.trust);
		descr.push("Parameters: " + $('<div/>').text(deal.params).html());
		descr.push("Beneficiary: " + deal.beneficiary);
		descr.push("Deadline: " + deadline);
		descr.push("Deadline reached: " + finished);

		$("#view-progress-deals").append(
			$("<a>")
			.attr("href", "#")
			.attr("data-toggle", "popover")
			.attr("title", title)
			.attr("data-content", descr.join("<br/>"))
			.attr("data-placement", "top")
			.addClass("progress-bar")
			.addClass(style)
			.width(width)
			.text((first+1) + " → " + last)
			.popover({ html: true })
		);

		for (var _ = 0; _ < parseInt(deal.botSize); ++idx, ++_)
		{
			var taskid = web3.utils.soliditySha3({ type: "bytes32", value: dealid }, { type: "uint256", value: idx });
			var task   = await IexecHub.methods.viewTask(taskid).call();
			tasks[idx] = { deal: deal, task: task };

			var status = parseInt(task.status);
			var style  = ["bg-secondary", "bg-primary progress-bar-striped progress-bar-animated", "bg-warning progress-bar-striped progress-bar-animated", "bg-success", "bg-danger"][status];
			var width  = (100 / volume) + "%";
			var title  = "Task " + (idx+1) + "/" + volume + ": " + ["Unset", "Active", "Revealing", "Completed", "Failed"][status];

			var descr = []
			if (status == 0) descr.push("Task waiting initialization");
			if (status >= 1) descr.push(task.contributors.length + " contributions received");
			if (status >= 2) descr.push("Consensus: " + task.consensusValue);
			if (status >= 2) descr.push("Reveal: " + task.revealCounter + "/" + task.winnerCounter);
			if (status == 1) descr.push("Contribution deadline: " + new Date(parseInt(task.contributionDeadline) * 1000));
			if (status == 2) descr.push("Reveal deadline: "       + new Date(parseInt(task.revealDeadline      ) * 1000));
			// if (status >= 1) descr.push("Final Deadline: "        + new Date(parseInt(task.finalDeadline       ) * 1000));
			if (status  < 3) descr.push("Final Deadline: "        + deadline);
			if (status  < 3 && finished)
			{
				descr.push("Deadline reached, task should be claimed");
				style = "bg-danger progress-bar-striped progress-bar-animated";
			}
			if (status >= 3) descr.push("Task has been finalized");

			$("#view-progress-tasks").append(
				$("<a>")
				.attr("href", "#")
				.attr("data-toggle", "popover")
				.attr("title", title)
				.attr("data-content", descr.join("<br/>"))
				.attr("data-placement", "bottom")
				.addClass("progress-bar")
				.addClass(style)
				.width(width)
				.text(idx+1)
				.popover({ html: true })
			);

		}
	}

	IexecClerk.methods.viewConsumed(hash).call().then(consumed => {
		first = last;
		last  = consumed;
		var style = "bg-danger progress-bar-striped";
		var width = ((parseInt(last) - first)*100/volume) + "%";
		var title = "Cancelled";
		var descr = [ "Task " + (first+1) + " → " + last ];

		if (last > first)
		{
			$("#view-progress-deals").append(
				$("<a>")
				.attr("href", "#")
				.attr("data-toggle", "popover")
				.attr("title", title)
				.attr("data-content", descr.join("<br/>"))
				.attr("data-placement", "top")
				.addClass("progress-bar")
				.addClass(style)
				.width(width)
				.text("Cancelled")
				.popover({ html: true })
			);
			$("#view-progress-tasks").append(
				$("<a>")
				.attr("href", "#")
				.attr("data-toggle", "popover")
				.attr("title", title)
				.attr("data-content", descr.join("<br/>"))
				.attr("data-placement", "bottom")
				.addClass("progress-bar")
				.addClass(style)
				.width(width)
				.text("Cancelled")
				.popover({ html: true })
			);
		}
	});
}

$("#view-submit").click(() => {
	try
	{
		__order = JSON.parse($("#view-input").val());
		if      (isValidOrder("AppOrder",        __order)) { __expand = false; __hash = AppOrderStructHash       (__order); }
		else if (isValidOrder("DatasetOrder",    __order)) { __expand = false; __hash = DatasetOrderStructHash   (__order); }
		else if (isValidOrder("WorkerpoolOrder", __order)) { __expand = false; __hash = WorkerpoolOrderStructHash(__order); }
		else if (isValidOrder("RequestOrder",    __order)) { __expand = true;  __hash = RequestOrderStructHash   (__order); }
		else throw "Invalid order";
	}
	catch (_)
	{
		__hash   = $("#view-input-hash").val();
		__expand = true;
	}
	finally
	{
		if (__hash != "")
		{
			IexecClerk.methods.viewConsumed(__hash).call().then(value => {
				__volume = typeof __order == "undefined" ? value : __order.volume;
				notify(" status: " + value + " / " + __volume);
				if (__expand)
				{
					RequestOrderProgress(__hash, __volume);
				}
			});
		}
	}
});

$("#match-submit").click(() => {
	__apporder        =                                        JSON.parse($("#match-apporder"       ).val());
	__datasetorder    = $("#match-datasetorder").val() != "" ? JSON.parse($("#match-datasetorder"   ).val()) : NULLDATASET
	__workerpoolorder =                                        JSON.parse($("#match-workerpoolorder").val());
	__requestorder    =                                        JSON.parse($("#match-requestorder"   ).val());
	if (!isValidOrder("DappOrder", __apporder       )) { alert("Invalid AppOrder"       ); return; }
	if (!isValidOrder("DataOrder", __datasetorder   )) { alert("Invalid DatasetOrder"   ); return; }
	if (!isValidOrder("PoolOrder", __workerpoolorder)) { alert("Invalid WorkerpoolOrder"); return; }
	if (!isValidOrder("UserOrder", __requestorder   )) { alert("Invalid RequestOrder"   ); return; }
	web3.eth.getAccounts().then(account => {
		IexecClerk.methods.matchOrders(__apporder, __datasetorder, __workerpoolorder, __requestorder)
		.send({ from: account[0], gas: 800000 })
		.then(console.log);
	});
});

$("#apporder-sign").click(() => {
	apporder = {
		app:                           $("#apporder-address"           ).val(),
		appprice:           parseFloat($("#apporder-price-value"       ).val()) * $("#apporder-price-unit").val(),
		volume:             parseInt  ($("#apporder-volume"            ).val()),
		tag:                           $("#apporder-tag"               ).val(),
		datasetrestrict:               $("#apporder-datasetrestrict"   ).val(),
		workerpoolrestrict:            $("#apporder-workerpoolrestrict").val(),
		requesterrestrict:             $("#apporder-requesterrestrict" ).val(),
		salt:                          $("#apporder-salt"              ).val(),
	};
	if (isNaN(apporder.appprice         )) { apporder.appprice           = 0;                                                                    }
	if (isNaN(apporder.volume           )) { apporder.volume             = 1;                                                                    }
	if (apporder.tag                == "") { apporder.tag                = "0x0000000000000000000000000000000000000000000000000000000000000000"; }
	if (apporder.datasetrestrict    == "") { apporder.datasetrestrict    = "0x0000000000000000000000000000000000000000";                         }
	if (apporder.workerpoolrestrict == "") { apporder.workerpoolrestrict = "0x0000000000000000000000000000000000000000";                         }
	if (apporder.requesterrestrict  == "") { apporder.requesterrestrict  = "0x0000000000000000000000000000000000000000";                         }
	if (apporder.salt               == "") { apporder.salt               = randomHex(32);                                                        }
	if (!web3.utils.isAddress(apporder.app               )) { alert("Invalid app address"               ); return;}
	if (!web3.utils.isAddress(apporder.datasetrestrict   )) { alert("Invalid datasetrestrict address"   ); return;}
	if (!web3.utils.isAddress(apporder.workerpoolrestrict)) { alert("Invalid workerpoolrestrict address"); return;}
	if (!web3.utils.isAddress(apporder.requesterrestrict )) { alert("Invalid requesterrestrict address" ); return;}
	(new web3.eth.Contract(AppABI, apporder.app)).methods.m_owner().call()
	.then(owner => {
		signStruct("AppOrder", apporder, owner)
		.then(signed => {
			console.log("apporder =", JSON.stringify(signed));
			$("#apporder-display").val(JSON.stringify(signed));
			notify("Apporder signature successfull")
		})
		.catch(console.log);
	})
	.catch(() => alert("Could not read app smartcontract"));
});

$("#datasetorder-sign").click(() => {
	datasetorder = {
		dataset:                       $("#datasetorder-address"           ).val(),
		datasetprice:       parseFloat($("#datasetorder-price-value"       ).val()) * $("#datasetorder-price-unit").val(),
		volume:             parseInt  ($("#datasetorder-volume"            ).val()),
		tag:                           $("#datasetorder-tag"               ).val(),
		apprestrict:                   $("#datasetorder-apprestrict"       ).val(),
		workerpoolrestrict:            $("#datasetorder-workerpoolrestrict").val(),
		requesterrestrict:             $("#datasetorder-requesterrestrict" ).val(),
		salt:                          $("#datasetorder-salt"              ).val(),
	};
	if (isNaN(datasetorder.datasetprice     )) { datasetorder.datasetprice       = 0;                                                                    }
	if (isNaN(datasetorder.volume           )) { datasetorder.volume             = 1;                                                                    }
	if (datasetorder.tag                == "") { datasetorder.tag                = "0x0000000000000000000000000000000000000000000000000000000000000000"; }
	if (datasetorder.apprestrict        == "") { datasetorder.apprestrict        = "0x0000000000000000000000000000000000000000";                         }
	if (datasetorder.workerpoolrestrict == "") { datasetorder.workerpoolrestrict = "0x0000000000000000000000000000000000000000";                         }
	if (datasetorder.requesterrestrict  == "") { datasetorder.requesterrestrict  = "0x0000000000000000000000000000000000000000";                         }
	if (datasetorder.salt               == "") { datasetorder.salt               = randomHex(32);                                                        }
	if (!web3.utils.isAddress(datasetorder.dataset           )) { alert("Invalid dataset address"           ); return;}
	if (!web3.utils.isAddress(datasetorder.apprestrict       )) { alert("Invalid apprestrict address"       ); return;}
	if (!web3.utils.isAddress(datasetorder.workerpoolrestrict)) { alert("Invalid workerpoolrestrict address"); return;}
	if (!web3.utils.isAddress(datasetorder.requesterrestrict )) { alert("Invalid requesterrestrict address" ); return;}
	(new web3.eth.Contract(DatasetABI, datasetorder.dataset)).methods.m_owner().call()
	.then(owner => {
		signStruct("DatasetOrder", datasetorder, owner)
		.then(signed => {
			console.log("datasetorder =", JSON.stringify(signed));
			$("#datasetorder-display").val(JSON.stringify(signed));
			notify("Datasetorder signature successfull")
		})
		.catch(console.log);
	})
	.catch(() => alert("Could not read dataset smartcontract"));
});

$("#workerpoolorder-sign").click(() => {
	workerpoolorder = {
		workerpool:                   $("#workerpoolorder-address"     ).val(),
		workerpoolprice:   parseFloat($("#workerpoolorder-price-value" ).val()) * $("#workerpoolorder-price-unit").val(),
		volume:            parseInt  ($("#workerpoolorder-volume"      ).val()),
		tag:                          $("#workerpoolorder-tag"         ).val(),
		category:          parseInt  ($("#workerpoolorder-category"    ).val()),
		trust:             parseInt  ($("#workerpoolorder-trust"       ).val()),
		apprestrict:                  $("#workerpoolorder-apprestrict").val(),
		datasetrestrict:              $("#workerpoolorder-datasetrestrict").val(),
		requesterrestrict:            $("#workerpoolorder-requesterrestrict").val(),
		salt:                         $("#workerpoolorder-salt"        ).val(),
	};
	if (isNaN(workerpoolorder.workerpoolprice )) { workerpoolorder.workerpoolprice   = 0;                                                                    }
	if (isNaN(workerpoolorder.volume          )) { workerpoolorder.volume            = 1;                                                                    }
	if (isNaN(workerpoolorder.category        )) { workerpoolorder.category          = 5;                                                                    }
	if (isNaN(workerpoolorder.trust           )) { workerpoolorder.trust             = 100;                                                                  }
	if (workerpoolorder.tag               == "") { workerpoolorder.tag               = "0x0000000000000000000000000000000000000000000000000000000000000000"; }
	if (workerpoolorder.apprestrict       == "") { workerpoolorder.apprestrict       = "0x0000000000000000000000000000000000000000";                         }
	if (workerpoolorder.datasetrestrict   == "") { workerpoolorder.datasetrestrict   = "0x0000000000000000000000000000000000000000";                         }
	if (workerpoolorder.requesterrestrict == "") { workerpoolorder.requesterrestrict = "0x0000000000000000000000000000000000000000";                         }
	if (workerpoolorder.salt              == "") { workerpoolorder.salt              = randomHex(32);                                                        }
	if (!web3.utils.isAddress(workerpoolorder.workerpool       )) { alert("Invalid workerpool address"      ); return;}
	if (!web3.utils.isAddress(workerpoolorder.apprestrict      )) { alert("Invalid apprestrict address"     ); return;}
	if (!web3.utils.isAddress(workerpoolorder.datasetrestrict  )) { alert("Invalid datasetrestrict address" ); return;}
	if (!web3.utils.isAddress(workerpoolorder.requesterrestrict)) { alert("Invalid requesterestrict address"); return;}
	(new web3.eth.Contract(WorkerpoolABI, workerpoolorder.workerpool)).methods.m_owner().call()
	.then(owner => {
		signStruct("WorkerpoolOrder", workerpoolorder, owner)
		.then(signed => {
			console.log("workerpoolorder =", JSON.stringify(signed));
			$("#workerpoolorder-display").val(JSON.stringify(signed));
			notify("Poolorder signature successfull")
		})
		.catch(console.log);
	})
	.catch(() => alert("Could not read workerpool smartcontract"));
});


$("#requestorder-sign").click(() => {
	requestorder = {
		app:                           $("#requestorder-app"                     ).val(),
		appmaxprice:        parseFloat($("#requestorder-appmaxprice-value"       ).val()) * $("#requestorder-appmaxprice-unit"       ).val(),
		dataset:                       $("#requestorder-dataset"                 ).val(),
		datasetmaxprice:    parseFloat($("#requestorder-datasetmaxprice-value"   ).val()) * $("#requestorder-datasetmaxprice-unit"   ).val(),
		workerpool:                    $("#requestorder-workerpool"              ).val(),
		workerpoolmaxprice: parseFloat($("#requestorder-workerpoolmaxprice-value").val()) * $("#requestorder-workerpoolmaxprice-unit").val(),
		volume:             parseInt  ($("#requestorder-volume"                  ).val()),
		tag:                           $("#requestorder-tag"                     ).val(),
		category:           parseInt  ($("#requestorder-category"                ).val()),
		trust:              parseInt  ($("#requestorder-trust"                   ).val()),
		requester:                     $("#requestorder-requester"               ).val(),
		beneficiary:                   $("#requestorder-beneficiary"             ).val(),
		callback:                      $("#requestorder-callback"                ).val(),
		params:                        $("#requestorder-params"                  ).val(),
		salt:                          $("#requestorder-salt"                    ).val(),
	};
	if (requestorder.dataset             == "") { requestorder.dataset            = "0x0000000000000000000000000000000000000000";                         }
	if (requestorder.workerpool          == "") { requestorder.workerpool         = "0x0000000000000000000000000000000000000000";                         }
	if (isNaN(requestorder.appmaxprice       )) { requestorder.appmaxprice        = 0;                                                                    }
	if (isNaN(requestorder.datasetmaxprice   )) { requestorder.datasetmaxprice    = 0;                                                                    }
	if (isNaN(requestorder.workerpoolmaxprice)) { requestorder.workerpoolmaxprice = 0;                                                                    }
	if (isNaN(requestorder.volume            )) { requestorder.volume             = 1;                                                                    }
	if (requestorder.tag                 == "") { requestorder.tag                = "0x0000000000000000000000000000000000000000000000000000000000000000"; }
	if (isNaN(requestorder.category          )) { requestorder.category           = 5;                                                                    }
	if (isNaN(requestorder.trust             )) { requestorder.trust              = 100;                                                                  }
	if (requestorder.beneficiary         == "") { requestorder.beneficiary        = requestorder.requester;                                               }
	if (requestorder.callback            == "") { requestorder.callback           = "0x0000000000000000000000000000000000000000";                         }
	if (requestorder.params              == "") { requestorder.params             = "\0";                                                                 }
	if (requestorder.salt                == "") { requestorder.salt               = randomHex(32);                                                        }
	if (!web3.utils.isAddress(requestorder.app        )) { alert("Invalid app address"        ); return;}
	if (!web3.utils.isAddress(requestorder.dataset    )) { alert("Invalid dataset address"    ); return;}
	if (!web3.utils.isAddress(requestorder.workerpool )) { alert("Invalid workerpool address" ); return;}
	if (!web3.utils.isAddress(requestorder.requester  )) { alert("Invalid requester address"  ); return;}
	if (!web3.utils.isAddress(requestorder.beneficiary)) { alert("Invalid beneficiary address"); return;}
	signStruct("RequestOrder", requestorder, requestorder.requester)
	.then(signed => {
		console.log("requestorder =", JSON.stringify(signed));
		$("#requestorder-display").val(JSON.stringify(signed));
		notify("Requestorder signature successfull")
	})
	.catch(console.log);
});

$("#cancel-submit").click(() => {
	__order = JSON.parse($("#cancel-input").val());
	if      (isValidOrder("AppOrder",        __order)) { __method = IexecClerk.methods.cancelAppOrder       (__order); }
	else if (isValidOrder("DatasetOrder",    __order)) { __method = IexecClerk.methods.cancelDatasetOrder   (__order); }
	else if (isValidOrder("WorkerpoolOrder", __order)) { __method = IexecClerk.methods.cancelWorkerpoolOrder(__order); }
	else if (isValidOrder("RequestOrder",    __order)) { __method = IexecClerk.methods.cancelRequestOrder   (__order); }
	getOrderOwner(__order).then(owner => {
		__method
		.send({ from: owner, gas: 80000 })
		.then(tx => {
				console.log(tx);
				notify("Order successfully cancelled");
		})
		.catch(e => {
			notify("Please switch wallet to " + owner);
		});
	});
});
