# === 4.3 新增：Excel 下载模块 ===
        with st.sidebar:
            st.divider()
            st.header("📥 导出审计详情")
            # 准备下载数据
            export_df = main_df.copy()
            
            # 构建输出列 (如果原文件没有剩余手牌/桌面列，填充 'N/A')
            export_cols = {
                '__ORIGIN__': '关卡ID',
                cm['jid']: '解集ID',
                # 这里的 cm[...] 获取的是原始列名
                cm['diff']: '难度',
                cm['act']: '实际结果',
                cm['rem_hand']: '剩余手牌',
                cm['rem_desk']: '剩余桌面牌',
                '最长连击': '最长连击',
                '长连次数': '长连次数',
                cm['seq']: '全部连击',
                '有效手牌': '有效手牌',
                cm['desk']: '初始桌面牌',
                cm['hand']: '初始手牌',
                '得分': '得分',
                '红线判定': '红线判定',
                '得分构成': '得分构成'
            }
            
            # 仅保留存在的列进行重命名和导出
            final_export_cols = {}
            for k, v in export_cols.items():
                if k is not None and k in export_df.columns:
                    final_export_cols[k] = v
                elif v in ['剩余手牌', '剩余桌面牌']: # 特殊处理可能不存在的列
                    export_df[v] = 'N/A'
                    final_export_cols[v] = v
            
            # 重命名列
            export_df = export_df.rename(columns=final_export_cols)
            
            # --- 【修复点：防止 '测试轮次' 已存在导致的报错】 ---
            if '测试轮次' in export_df.columns:
                export_df = export_df.drop(columns=['测试轮次'])
            # -----------------------------------------------

            # 添加测试轮次 (1-based index)
            export_df.insert(2, '测试轮次', range(1, 1 + len(export_df)))
            
            # 筛选最终输出列
            target_cols = ['关卡ID', '解集ID', '测试轮次', '难度', '实际结果', '剩余手牌', '剩余桌面牌', 
                           '最长连击', '长连次数', '全部连击', '有效手牌', '初始桌面牌', '初始手牌', 
                           '得分', '红线判定', '得分构成']
            # 确保列存在 (防止某些特殊情况下列丢失)
            target_cols = [c for c in target_cols if c in export_df.columns]
            
            # 转换为CSV (Excel兼容格式)
            csv_data = export_df[target_cols].to_csv(index=False).encode('utf-8-sig')
            
            st.download_button(
                label="📄 下载完整审计明细 (Excel)",
                data=csv_data,
                file_name="Tripeaks_Audit_Details.csv",
                mime="text/csv"
            )
