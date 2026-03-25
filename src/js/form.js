/**
 * 表单组件
 */
Vue.component('el-form-message', {
	template: `
	<el-form 
		class="el-form-message"
		v-if="form.status === 1"
		:model="content" 
		:rules="rules" 
		ref="content" 
		:label-width="form.label_width" 
		:label-position="form.label_position">
		<el-form-item 
			v-for="(item, index) in field" 
			:key="index"
			:class="item.field"
			:label="form.label_width === 0 || item.show === 0 ? '' : lang(item.field)"
			:prop="item.field">
			<component 
	            v-model="content[item.field]" 
	            :is="item.type.is" 
	            :key="item.field" 
	            :type="item.type.type" 
	            :options="region"
	            :placeholder="lang(item.placeholder)">
	            <template v-if="typeof item.type.child !== 'undefined'">
	                <component
	                    :is="item.type.child.is"
	                    v-for="(value, index) in item.type.child.value"
	                    :key="index"
	                    :label="value"
	                    :value="value">
	                    {{value}}
	                </component>
	            </template>
	        </component>
		</el-form-item>
		<el-form-item 
			class="captcha"
			v-if="form.captcha === 1" 
			:label="form.label_width === 0 ? '' : lang('verification code')" 
			prop="captcha">
			<img 
                class="el-message-captcha" 
                :src="captcha" 
                @click="getCaptcha()" />
            <el-input
                class="el-message-code" 
                v-model="content.captcha" 
                :placeholder="lang('Please enter the verification code')"
                @keyup.enter.native="submitForm()">
            </el-input>
		</el-form-item>
		<el-form-item class="submit">
			<el-button @click="submitForm()" :loading="submitLoading">{{form.submit_title}}</el-button>
		</el-form-item>
	</el-form>
	`,
	props: {
		id: {
			type: Number,
			required: true
		},
	},
	data() {
		return {
			indexUrl: 'form/form/index',
			submitUrl: 'form/form/submit',
			form: {},
			field: {},
			content: {},
			captcha: "",
			loading: false,
			submitLoading: false,
		}
	},
	created() {
		this.getForm();
	},
	computed: {
		rules() {
			let rules = {};
			this.field.forEach(function (item, index) {
				rules[item.field] = [];
				if (item.request === 1) {
					rules[item.field].push({ required: true, message: '不能为空', trigger: 'blur' });
				}
				if (item.rule !== '') {
					rules[item.field].push({pattern: item.rule, message: '输入格式不正确'});
				}
			})
			return rules;
		},
	},
	methods: {
		/**
		 * 获取表单
		 */
		getForm() {
			let self = this;
			request.post(self.indexUrl, {id: self.id}, function(res) {
				if (res.status === 'success') {
					self.form = res.data;
					self.field = self.form.field;
					if (self.form.captcha === 1) {
						self.getCaptcha();
					}
					let content = {};
					self.field.forEach(function (item, index) {
						content[item.field] = item.type.value;
					});
					self.content = content;
				}
			});
		},
		/**
         * 获取验证码
         */
        getCaptcha() {
        	let link = url('verify');
            let str  = link.indexOf('?') === -1 ? '?' : '&';
            this.captcha = link + str + Math.random();
        },
		/**
		 * 提交表单
		 */
		submitForm() {
			let self = this;
			self.$refs.content.validate((valid) => {
                if (valid) {
                	self.submitLoading = true;
					request.post(self.submitUrl, {id: self.id, content: self.content, source: window.location.href, captcha: self.content.captcha}, function(res) {
						self.$message({ showClose: true, message: res.message, type: res.status });
						self.getCaptcha();
						self.submitLoading = false;
						if (res.status === 'success') {
	                        self.$refs.content.resetFields();
						} else {
							self.content.captcha = "";
						}
					});
                } else {
                    return false;
                }
            });
		},
	}
});