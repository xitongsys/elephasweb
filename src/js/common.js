/**
 * 全局状态
 */
var store = {
    debug: false,
    state: {
        loginDialog: false,
    },
    setLoginDialog (newValue) {
        this.state.loginDialog = newValue
    },
}

/**
 * 网络请求(全局使用此方法进行请求接口)
 */
var request = {
	/**
	 * 发送post请求
	 * @param  {String} url   链接
	 * @param  {Object} data  数据集
	 */
	post(link, data, callback = ""){
		$.ajax({
			url: url(link),
			type: 'post',
			dataTyle: 'json',
			data: data,
			success:function(res) {
				var res = typeof res == 'string' ? JSON.parse(res) : res;
				if (res.status === 'login') {
					store.setLoginDialog(true); // 打开登录弹窗
					if (callback != "") callback(res);
				} else {
					if (callback != "") callback(res);
				}
			},
			error:function(res) {
				res.status  = 'error';
				res.message = res.statusText;
				if (callback != "") callback(res);
			}
		})
	},
}