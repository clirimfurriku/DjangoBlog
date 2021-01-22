async function SwitchStar(productID, likeType, toIncrementID) {
    let likeCount;
    const response = await fetch('/action/like/' + likeType + '/' + productID.toString().replace(likeType + "-", ""), {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
    }).catch(
        () => {
            M.toast({html: 'Network error while checking star state', classes: 'rounded'});
        }
    );
    const response_json = await response.json();
    const star = document.getElementById(productID);
    if (response_json.status === "unliked") {
        star.firstElementChild.innerText = "favorite_border"
        if (toIncrementID !== void 0) {
            likeCount = document.getElementById(toIncrementID);
            likeCount.innerText--
        }
        M.toast({
            html: likeType.charAt(0).toUpperCase() + likeType.slice(1) + ' Like Removed',
            classes: 'rounded'
        });
    } else if (response_json.status === "liked") {
        star.firstElementChild.innerText = "favorite"
        if (toIncrementID !== void 0) {
            likeCount = document.getElementById(toIncrementID);
            likeCount.innerText++
        }
        M.toast({html: likeType.charAt(0).toUpperCase() + likeType.slice(1) + ' Liked', classes: 'rounded'});
    }
}

async function Report(productID, reportType) {
    const response = await fetch('/action/report/' + reportType + '/' + productID.toString().replace(reportType + "-report-", ""), {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
    }).catch(
        () => {
            M.toast({html: 'Network error while checking star state', classes: 'rounded'});
        }
    );
    const response_json = await response.json();
    if (response_json.status === "exists") {
        M.toast({
            html: 'You have already reported this ' + reportType.charAt(0).toUpperCase() + reportType.slice(1),
            classes: 'rounded'
        });
    } else if (response_json.status === "reported") {
        M.toast({
            html: reportType.charAt(0).toUpperCase() + reportType.slice(1) + ' Report has been sent to our staff for review',
            classes: 'rounded'
        });
    }
}