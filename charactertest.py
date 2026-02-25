# 医学生健康行为标准化测评 - 网页版（Streamlit）
import streamlit as st

# ---------------------- 问卷配置（完全匹配你的原始规则） ----------------------
question_list = [
    [1, "1. 我能保持规律的作息，每日入睡/起床时间波动不超过30分钟", "正向", "睡眠行为维度"],
    [2, "2. 期末/备考/值班期间，我不会刻意压缩睡眠时间到6小时以内", "正向", "睡眠行为维度"],
    [3, "3. 我能保持三餐规律，不会长期不吃早餐/晚餐", "正向", "饮食行为维度"],
    [4, "4. 期末/备考/值班期间，我不会长期只吃外卖/速食，忽略饮食均衡", "正向", "饮食行为维度"],
    [5, "5. 我能保持规律的运动习惯，每周至少有2次及以上的身体活动", "正向", "运动行为维度"],
    [6, "6. 期末/备考/值班期间，我不会完全停止所有运动行为", "正向", "运动行为维度"],
]

option_desc = ["完全不符合（0分）", "偶尔符合（2分）", "基本符合（4分）", "完全符合（6分）"]
option_score = [0, 2, 4, 6]

suggestion_dict = {
    "睡眠行为维度": "【睡眠维度干预建议】\n1. 值班/备考期间，固定起床时间，即使熬夜也不晚起超过1小时，维持生物钟稳定；\n2. 夜班后补觉不超过30分钟，避免打乱夜间睡眠；\n3. 睡前1小时远离手机/电脑，用5分钟正念呼吸降低入睡难度。",
    "饮食行为维度": "【饮食维度干预建议】\n1. 值班/实验前提前准备便携健康餐（全麦面包、鸡蛋、坚果），避免忙到错过正餐；\n2. 外卖优先选「清炒/蒸煮」菜品，搭配1份蔬菜，避免长期高油高盐；\n3. 随身带无糖酸奶/水果，替代奶茶、油炸零食。",
    "运动行为维度": "【运动维度干预建议】\n1. 利用碎片化时间做微运动：查房间隙5分钟靠墙拉伸、课间3分钟开合跳、写病历间隙肩颈放松；\n2. 值班/备考期间，每周2次10分钟居家无器械运动，无需专门去健身房；\n3. 通勤时提前1站下车步行，累计日常活动量。"
}

# ---------------------- 页面基础配置 ----------------------
st.set_page_config(page_title="医学生健康行为测评", page_icon="🏥", layout="centered")
st.title("🏥 医学生健康行为标准化测评")
st.divider()
st.markdown("📋 填写说明：共6道题，选择符合你的选项，提交后自动生成健康画像与专属干预建议")

# ---------------------- 渲染测评问卷 ----------------------
st.subheader("📝 测评问卷")
user_answers = []
for q in question_list:
    q_id, q_content, q_type, q_dimension = q
    answer = st.radio(
        label=q_content,
        options=option_desc,
        index=None,
        key=f"q_{q_id}"
    )
    user_answers.append(answer)

# ---------------------- 提交按钮与结果计算 ----------------------
st.divider()
submit_btn = st.button("✅ 提交并生成测评结果", type="primary", use_container_width=True)

if submit_btn:
    # 校验是否完成所有题目
    if None in user_answers:
        st.warning("⚠️ 请完成所有题目后再提交！")
    else:
        # 计算各维度得分
        score_dict = {"睡眠行为维度": 0, "饮食行为维度": 0, "运动行为维度": 0}
        for i, q in enumerate(question_list):
            q_dimension = q[3]
            raw_score = option_score[option_desc.index(user_answers[i])]
            final_score = raw_score
            score_dict[q_dimension] += final_score
        total_score = sum(score_dict.values())

        # 匹配健康画像
        if total_score >= 24:
            user_type = "标杆维持型（低年级高重视度）/结构优化型（高年级高重视度）"
            type_desc = "✅ 你的健康行为整体表现优秀，有良好的健康习惯和重视度。建议继续保持现有习惯，针对个别小短板做精细化优化，进一步巩固健康状态。"
        elif 12 <= total_score <= 23:
            user_type = "潜力待挖型（高年级低重视度）"
            type_desc = "💡 你有基础的健康意识，但执行度仍有提升空间，属于典型的「知行有差距」群体。建议针对核心短板，用场景化微动作降低执行门槛，逐步养成稳定的健康习惯。"
        else:
            user_type = "短板突破型（低年级低重视度）"
            type_desc = "⚠️ 你的健康行为存在明显短板，健康习惯的稳定性不足。建议优先聚焦1-2个核心短板，从最简单的微动作开始突破，逐步建立健康行为的正反馈。"

        # 识别核心干预短板（≤4分）
        weak_dimension = [dim for dim, score in score_dict.items() if score <= 4]

        # 渲染最终结果
        st.divider()
        st.header("📊 你的测评结果")
        st.subheader("📈 各维度得分")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="睡眠行为维度", value=f"{score_dict['睡眠行为维度']}/12分")
        with col2:
            st.metric(label="饮食行为维度", value=f"{score_dict['饮食行为维度']}/12分")
        with col3:
            st.metric(label="运动行为维度", value=f"{score_dict['运动行为维度']}/12分")

        st.metric(label="🎯 总得分", value=f"{total_score}/36分")
        st.divider()

        st.subheader("🏷️  你的健康画像")
        st.success(f"**{user_type}**")
        st.markdown(type_desc)
        st.divider()

        if weak_dimension:
            st.subheader("🎯 核心干预短板")
            st.error(f"{','.join(weak_dimension)}")
            st.subheader("📋 专属干预建议")
            for dim in weak_dimension:
                st.markdown(suggestion_dict[dim])
        else:
            st.success("🎉 恭喜！你没有核心干预短板，各维度表现均衡，继续保持现有健康习惯即可！")