async function loadDashboard(){

    const response = await fetch("/api/interfaces");

    const data = await response.json();

    // Summary

    document.getElementById("totalPorts").innerText =
        data.summary.total_ports;

    document.getElementById("portsUp").innerText =
        data.summary.ports_up;

    document.getElementById("portsDown").innerText =
        data.summary.ports_down;

    document.getElementById("totalRx").innerText =
        data.summary.total_rx.toFixed(2)+" Mbps";

    document.getElementById("totalTx").innerText =
        data.summary.total_tx.toFixed(2)+" Mbps";

    document.getElementById("lastUpdate").innerText =
        new Date().toLocaleTimeString();

    const tbody=document.getElementById("tableBody");

    tbody.innerHTML="";

    const search=document.getElementById("search")
                    .value
                    .toLowerCase();

    data.interfaces.forEach(port=>{

        if(!port.interface.toLowerCase().includes(search))
            return;

        let color="greenFill";

        const util=Math.max(port.rx_util,port.tx_util);

        if(util>70)
            color="redFill";
        else if(util>40)
            color="yellowFill";

        const row=`
        <tr>

        <td>${port.interface}</td>

        <td>
            <span class="status ${port.status=="UP"?"up":"down"}">
            ${port.status}
            </span>
        </td>

        <td>
            <span class="speed">
            ${port.speed} Mbps
            </span>
        </td>

        <td>${port.rx_mbps.toFixed(2)}</td>

        <td>${port.tx_mbps.toFixed(2)}</td>

        <td>

            <div class="bar">

                <div class="fill ${color}"
                     style="width:${Math.min(port.rx_util,100)}%">

                    ${port.rx_util.toFixed(2)}%

                </div>

            </div>

        </td>

        <td>

            <div class="bar">

                <div class="fill ${color}"
                     style="width:${Math.min(port.tx_util,100)}%">

                    ${port.tx_util.toFixed(2)}%

                </div>

            </div>

        </td>

        </tr>
        `;

        tbody.innerHTML+=row;

    });

}

document.getElementById("search").addEventListener("keyup",loadDashboard);

loadDashboard();

setInterval(loadDashboard,5000);
