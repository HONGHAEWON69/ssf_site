import streamlit as st
import pandas as pd

# --------------------------------------------------------------------------
# 0. 페이지/스타일 설정
# --------------------------------------------------------------------------
st.set_page_config(page_title="서울 장학금 추천", page_icon="🎓", layout="wide")

# 연노랑 버튼/카드 스타일 (컴팩트 레이아웃)
st.markdown("""
<style>
  .stApp { background-color:#ffd240; }
  .card {
    background:#fff; border:1px solid #e5e7eb; border-radius:12px;
    padding:14px; box-shadow:0 3px 10px rgba(0,0,0,.04); margin-bottom:8px;
  }
  .pill {
    display:inline-block; padding:3px 8px; border-radius:999px; font-size:12px;
    background:#fff7ed; color:#7c2d12; border:1px solid #fed7aa; margin-right:6px; margin-bottom:6px;
  }
  /* 연노랑 버튼 (두 버튼 모두 동일 색상) */
  .btn-yellow {
    display:inline-block; text-decoration:none !important;
    background:#FFE999; color:#3a3a00 !important; font-weight:700;
    padding:8px 10px; border-radius:8px; border:1px solid #E6D77A;
    font-size:13px; line-height:1; white-space:nowrap;
  }
  .btn-row { display:flex; gap:8px; align-items:center; margin:6px 0 0; }
  /* 표 컨테이너도 컴팩트하게 */
  div[data-testid="stDataFrame"] > div:nth-child(1) {
    border-radius:10px; overflow:hidden; border:1px solid #E6E8EF;
    box-shadow:0 3px 10px rgba(0,0,0,.04);
  }
  /* 구분선 간격 축소 */
  .compact-hr { border:none; border-top:1px solid #e5e7eb; margin:10px 0; }
  /* 하단 안내 섹션도 한 줄로 */
  .footer-inline { display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# 1. 장학금 데이터베이스 (+ url 필드)
#    ※ url은 플레이스홀더 → 실제 상세 페이지 URL로 교체하세요.
# --------------------------------------------------------------------------
def create_scholarship_df():
    data = [
        # 대학원생
        {'장학금명': 'AI서울테크 대학원 장학금', '구분': '대학원생', '학년 정보': '대학원 재학생',
         '전공 계열': 'AI/이공계', '필수 조건': '해당 없음', '경제상황 요건': '해당 없음',
         'url': 'https://www.hissf.or.kr/'},  # TODO

        # 대학생
        {'장학금명': '서울희망 대학진로 장학금', '구분': '대학생',
         '학년 정보': '신입생(1학년), 재학생(2학년 이상)', '전공 계열': '전공무관',
         '필수 조건': '해당 없음',
         '경제상황 요건': '기초생활수급자/법정차상위계층, 학자금지원 4구간 이내',
         'url': 'https://www.hissf.or.kr/'},  # TODO

        {'장학금명': '서울희망 공익인재 장학금', '구분': '대학생',
         '학년 정보': '재학생(2학년 이상)', '전공 계열': '전공무관',
         '필수 조건': '사회공헌활동 경험자', '경제상황 요건': '해당 없음',
         'url': 'https://www.hissf.or.kr/'},  # TODO

        {'장학금명': '독립유공자 후손 장학금', '구분': '대학생',
         '학년 정보': '신입생(1학년), 재학생(2학년 이상)', '전공 계열': '전공무관',
         '필수 조건': '독립유공자 후손 (4~6대)', '경제상황 요건': '해당 없음',
         'url': 'https://www.hissf.or.kr/'},  # TODO

        {'장학금명': '서울 해외교환학생 장학금', '구분': '대학생',
         '학년 정보': '재학생(2학년 이상)', '전공 계열': '전공무관',
         '필수 조건': '해외교환학생으로 선발된 자',
         '경제상황 요건': '기초생활수급자/법정차상위계층, 학자금지원 4구간 이내',
         'url': 'https://www.hissf.or.kr/'},  # TODO

        {'장학금명': '청춘Start 장학금', '구분': '대학생',
         '학년 정보': '신입생(1학년)', '전공 계열': '전공무관', '필수 조건': '해당 없음',
         '경제상황 요건': '기초생활수급자/법정차상위계층, 아동복지시설 퇴소자',
         'url': 'https://www.hissf.or.kr/'},  # TODO

        {'장학금명': '서울희망 직업전문학교 장학금', '구분': '대학생',
         '학년 정보': '직업전문학교 학생', '전공 계열': '전공무관', '필수 조건': '해당 없음',
         '경제상황 요건': '기초생활수급자/법정차상위계층',
         'url': 'https://www.hissf.or.kr/'},  # TODO

        # 고등학생
        {'장학금명': '서울희망고교진로 장학금', '구분': '고등학생',
         '학년 정보': '고등학교 재학생', '전공 계열': '전공무관', '필수 조건': '해당 없음',
         '경제상황 요건': '기초생활수급자, 차상위계층, 북한이탈주민, 경제사각지대',
         'url': 'https://www.hissf.or.kr/'},  # TODO

        {'장학금명': '서울희망 예체능 장학금', '구분': '고등학생',
         '학년 정보': '고등학교 재학생', '전공 계열': '예체능', '필수 조건': '예체능 특기자',
         '경제상황 요건': '기초생활수급자/법정차상위계층, 학교장 추천 받은 학생',
         'url': 'https://www.hissf.or.kr/'},  # TODO

        {'장학금명': '서울꿈길장학금', '구분': '고등학생',
         '학년 정보': '비인가 대안교육기관 재학 청소년', '전공 계열': '전공무관', '필수 조건': '학교장 추천',
         '경제상황 요건': '기초생활수급자/법정차상위계층, 학교장 추천',
         'url': 'https://www.hissf.or.kr/'}   # TODO
    ]
    return pd.DataFrame(data)

# --------------------------------------------------------------------------
# 2. 결과 출력 함수 (카드 + 두 개 버튼 + 표, 컴팩트)
# --------------------------------------------------------------------------
def display_results(result_df):
    st.subheader("🏆 추천 장학금 결과")
    if result_df.empty:
        st.info("✅ 아쉽지만 현재 조건에 맞는 장학금이 없습니다.")
        return

    st.success(f"총 {len(result_df)}개의 장학금을 추천합니다!")

    # (1) 요청한 '장학금 신청하기' 공식 링크로 교체
    APPLY_URL = "https://www.hissf.or.kr/home/kor/M821806781/scholarship/business/index.do"

    for _, row in result_df.iterrows():
        # 카드 본문
        st.markdown(
            f"""
            <div class="card">
              <h4 style="margin:0 0 6px 0;">🎓 {row['장학금명']}</h4>
              <div style="color:#6b7280; font-size:13px; margin-bottom:6px;">
                {row.get('구분','')} · {row.get('학년 정보','')}
              </div>
              <div style="margin-bottom:6px;">
                <span class="pill">전공: {row.get('전공 계열','-')}</span>
                <span class="pill">필수: {row.get('필수 조건','-')}</span>
                <span class="pill">경제: {row.get('경제상황 요건','-')}</span>
              </div>
              <div class="btn-row">
                <!-- (2) 두 버튼 모두 연노랑 + 목적지 텍스트 + 이모지 -->
                <a class="btn-yellow" href="{APPLY_URL}" target="_blank">서울장학재단 ‘신청 페이지’로 이동 🚀</a>
            """,
            unsafe_allow_html=True
        )

        # 자세히 보기 버튼: url 유효 시에만 노출
        detail_url = row.get("url", "")
        if isinstance(detail_url, str) and detail_url.startswith(("http://", "https://")):
            st.markdown(
                f'<a class="btn-yellow" href="{detail_url}" target="_blank">해당 장학금 ‘안내 페이지’로 이동 ↗</a></div></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<span class="btn-yellow" style="opacity:.6;">안내 페이지 URL 준비 중 🙏</span></div></div>',
                unsafe_allow_html=True
            )

    # 표(컴팩트)
    with st.expander("📋 표로 보기"):
        result_df_display = result_df.drop(columns=['구분', '학년 정보'], errors='ignore')
        st.dataframe(result_df_display, hide_index=True, use_container_width=True)

    # (3) 하단 안내도 한 줄 구성 → 한 화면에 들어오게 여백 최소화
    st.markdown('<hr class="compact-hr" />', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="footer-inline">
          <span style="font-size:13px; color:#374151;">🔗 더 많은 장학금 정보는 서울장학재단 공식 홈페이지에서 확인하세요.</span>
          <a class="btn-yellow" href="https://www.hissf.or.kr/" target="_blank">서울장학재단 ‘홈페이지’로 이동 🏠</a>
          <a class="btn-yellow" href="https://www.hissf.or.kr/home/kor/M821806781/scholarship/business/index.do" target="_blank">서울장학재단 ‘신청 페이지’로 이동 🚀</a>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------------------------------
# 3. 메인 프로그램 로직 (네 로직 유지)
# --------------------------------------------------------------------------
def create_scholarship_df_base():
    # 기존 함수명과 충돌 방지용 (혹시 외부에서 가져다 쓸 때 대비)
    return create_scholarship_df()

def main():
    df = create_scholarship_df_base()

    st.title("✨ 나에게 맞는 서울 장학금 추천")
    st.write("간단한 질문에 답변하고, 나에게 딱 맞는 장학금을 찾아보세요!")

    main_type = st.selectbox("학생 구분을 선택해주세요.", ['--선택--', '대학원생', '대학생', '고등학생'])
    if main_type == '--선택--':
        return

    if main_type == '대학원생':
        display_results(df[df['구분'] == '대학원생'])
        return

    if main_type == '대학생':
        status_options = ['--선택--', '신입생(1학년)', '재학생(2학년 이상)', '직업전문학교 학생']
        user_status = st.selectbox("학년 정보를 선택해주세요.", status_options)
        if user_status == '--선택--':
            return

        if user_status == '직업전문학교 학생':
            result_df = df[df['장학금명'] == '서울희망 직업전문학교 장학금']
            display_results(result_df); return

        if user_status == '신입생(1학년)':
            names = ['서울희망 대학진로 장학금', '청춘Start 장학금', '독립유공자 후손 장학금']
            result_df = df[df['장학금명'].isin(names)]
            display_results(result_df); return

        if user_status == '재학생(2학년 이상)':
            excluded = ['청춘Start 장학금', '서울희망 직업전문학교 장학금']
            result_df = df[(df['구분'] == '대학생') & (~df['장학금명'].isin(excluded))]
            display_results(result_df); return

    elif main_type == '고등학생':
        status_options = ['--선택--', '고등학교 재학생', '비인가 대안교육기관 재학 청소년']
        user_status = st.selectbox("조금 더 상세한 신분을 선택해주세요.", status_options)
        if user_status == '--선택--':
            return

        if user_status == '비인가 대안교육기관 재학 청소년':
            display_results(df[df['학년 정보'] == user_status]); return

        filtered_df = df[df['학년 정보'] == user_status]

        user_major = st.selectbox("전공 계열을 선택해주세요.", ['--선택--', '예체능', '기타'])
        if user_major == '--선택--':
            return

        eco_options = [
            '--선택--', '기초생활수급자 또는 법정차상위계층', '북한이탈주민',
            '위에 해당하지 않지만 경제적 지원이 필요한 상황 (경제사각지대 등)', '해당 없음'
        ]
        user_eco_choice = st.selectbox("경제적 상황을 선택해주세요.", eco_options)
        if user_eco_choice == '--선택--':
            return

        user_eco_conditions = []
        if user_eco_choice == eco_options[1]:
            user_eco_conditions = ['기초생활수급자', '차상위계층', '법정차상위계층']
        elif user_eco_choice == eco_options[2]:
            user_eco_conditions = ['북한이탈주민']
        elif user_eco_choice == eco_options[3]:
            user_eco_conditions = ['경제사각지대', '학교장 추천 받은 학생']

        final_recommendations = []
        for _, row in filtered_df.iterrows():
            if user_major == '예체능' and row['전공 계열'] != '예체능':
                continue
            if user_major == '기타' and row['전공 계열'] == '예체능':
                continue

            req_eco = row['경제상황 요건']
            if user_eco_choice == '해당 없음':
                if '해당 없음' in row['필수 조건'] and '해당 없음' in req_eco:
                    final_recommendations.append(row)
            elif any(cond in req_eco for cond in user_eco_conditions):
                final_recommendations.append(row)

        display_results(pd.DataFrame(final_recommendations))

# --------------------------------------------------------------------------
# 4. 실행
# --------------------------------------------------------------------------
if __name__ == "__main__":
    main()
