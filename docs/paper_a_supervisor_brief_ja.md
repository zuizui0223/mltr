# Paper A 指導教員レビュー用 brief

## まず伝えたい結論

Paper A は、当初の「新しい coarsest source-relative repair 定理」を主張する theorem-first 論文から、**構造変化後に既存の生態学的状態分類を管理判断へ再利用してよいかを監査し、失敗した場合に何を観測すべきかを特定する理論**へ全面的に組み替えた。

現在の中心問いは：

> ある生態系管理で既に使われている状態分類は、種の入れ替わり・相互作用の再配線・生息地変化・新しい介入の導入後にも、管理判断に必要な情報を十分保持しているか。保持していないなら、何を追加して区別・観測すれば decision-sufficient な状態表現を回復できるか。

## 先行研究精査で撤回した新規性

以下は既知として本文・補足で明示的に位置づけ直した。

- 任意の初期分割からの coarsest stable refinement：Paige & Tarjan (1987)
- MDP の coarsest homogeneous refinement：Givan, Dean & Greig (2003)
- MDP state abstraction の体系化：Li, Walsh & Littman (2006)
- source MDP から target MDP への state abstraction transfer：Walsh, Li & Littman (2006)
- 異なる decision process 間の homomorphism：Ravindran & Barto (2003)
- state-and-transition model を用いた targeted monitoring：Jones et al. (2023)
- 生態学的 value of information：Canessa et al. (2015)
- history-preserving / path-sensitive formalism：既存分野として認識
- state identification / sensor-selection / set-cover 型の観測選択：一般的な形式・制御分野に既存

したがって、**generic refinement、generic abstraction transfer、targeted monitoring、VoI、history-sensitive equivalence、set-cover 自体を新規とは主張しない**。

## 現在主張する貢献

1. **Decision-sufficiency audit**
   - inherited state 内で target の output、実施可能 action、action 後の successor state が一様かを検査する。
   - 一様なら旧分類をそのまま管理へ使える。

2. **Local obstruction**
   - 旧分類が失敗するとき、「同じ旧stateなのにtarget actionへの応答が異なる」具体的な状態対を返す。

3. **Monitoring realization criterion**
   - candidate measurement `z_j` の集合 `S` が repaired state `Q*` を実現するとは、`C` と `z_S` から `Q*` を復元する decoder が存在することと定義した。
   - これは、旧分類では同じだが `Q*` では異なる全 obstruction pair を、選択測定の少なくとも1つが分離することと必要十分。
   - したがって最小費用monitoringは weighted set-cover になり、候補変数全体でも分離できない pair は **このmeasurement libraryでは修復不能**という明示的certificateになる。

4. **repair の意味を分離**
   - structural state-count defect
   - distribution-sensitive conditional information
   - monitoring realization cost
   - decision regret / downstream VoI
   - 「state が多く増えるほど生態学的影響が大きい」とは主張しない。

5. **route context**
   - 異なる replacement route が同じ terminal state meaning を運ぶなら history は捨てる。
   - incompatible な carried map を運ぶ場合だけ immutable context を残す。

## 指摘されていた未証明4点は現在どうなったか

### 1. Minimum conditional label information — 証明済み

任意の exact refinement `P` は coarsest exact repair `Q*` を refine するため、`Q*` は `P` の決定論的関数になる。条件付きentropyのchain ruleから

`H(Q*|C) <= H(P|C)`

を証明し、各 inherited class 内の repaired block 数 `k_c` による上界も証明した。

### 2. Monitoring realization — 必要十分条件として証明済み

`Q*(x)=d_S(C(x),z_S(x))` を満たすdecoderの存在を定義し、

- decoderが存在するなら全 obstruction pair は選択測定で分離される
- 全 obstruction pair が分離されるなら decoder を well-defined に構成できる

を両方向で証明した。

さらに minimum-cost realization と infeasibility certificate を系として示した。**現在の生態学的中心結果はここ。**

### 3. No universal defect-regret ordering — 強い形で証明済み

分類 `P` から選べる最適管理価値 `V_mu(P;u)` と

`R_mu(C,Q*;u)=V_mu(Q*;u)-V_mu(C;u)`

を定義した。

さらに、任意の整数 `d>=1` と任意の `r>=0` に対し、

`|Q*|-|C|=d` かつ `regret=r`

となる有限 target system を構成した。したがって state-count defect だけでは regret の非自明な上限・正の下限・単調ランキングのいずれも与えられない。

### 4. Source-relative exact repair — 外部定理への依存を解消

Paige–Tarjan / Givan–Dean–Greig をブラックボックスとして proof に使う形をやめた。本稿の有限 setting について、output・legal action・successor block を含む refinement signature を明示し、

1. refinement が有限回で停止すること
2. fixed point が exact であること
3. 任意の exact refinement が全 iteration を refine すること
4. よって fixed point が unique coarsest exact refinement であること

を自己完結に証明した。

Paige–Tarjan / Givan–Dean–Greig は **「この一般構成は既知であり、本稿の数学的新規性ではない」ことを示す引用**としてのみ使う。

## 植物–送粉者例で何が起きるか

旧分類では Site A と B が同じ pollination state にまとめられている。

pollinator turnover 後、新しい介入が substitute-pollinator response の違いを露出すると、A と B を同じ管理stateとして扱えなくなる。local obstruction は A--B pair であり、修復後に区別すべき生態学的差は substitute-response capacity になる。

illustrative decision layer として：

- benefit `B=1`
- `c_A=0.20`, `c_B=0.35`
- `p_A=0.25`, `p_B=0.80`

を置くと、旧 pooled state は安い A を選ぶが、repair 後は B を選ぶ。旧判断の one-step regret は `0.40`。一般的な逆転条件は

`p_B - p_A > (c_B - c_A)/B`

であり、実証推定値ではなく sensitivity example と明記している。

## 論文の構造的リスク

proof gap はかなり閉じた。一方、**generic な数学的新規性を主張しない以上、採否は生態学的問題設定の一般性と重要性に強く依存する**という評価は変わらない。

ただし現在は framing だけではない。Monitoring realization criterion が、audit failure を以下の実務出力へ変換する：

- inherited state の pass/fail
- failure を示す obstruction pair
- candidate measurement library が repaired state を実現可能かの必要十分判定
- 不可能な場合の explicit obstruction certificate
- 可能な場合の minimum-cost measurement selection

Jones et al. (2023) は predefined state を区別する観測変数を選ぶ。本稿はその一段上流で、**predefined state 自体が新しい介入に対してまだ妥当かを検査し、失効したときに初めて区別すべきpairを生成する**。Canessa et al. (2015) の VoI はさらに下流で、その情報を取得する価値を評価する。

したがって現在の最も防御可能なストーリーは：

`inherited management state -> structural audit -> obstruction -> monitoring feasibility/cost -> decision consequence`

である。

## 現在の推奨

Theoretical Ecology を第一候補のままにするが、本文では Monitoring realization を applied centerpiece にする。`coarsest refinement` や `transport defect` をheadlineに戻さない。

教員に本当に判断してほしいのは次の2点だけ：

1. **この「既存の管理stateが構造変化後もdecision-sufficientかを監査し、失敗をmonitoring requirementへ変換する」という問いは、Theoretical Ecology で独立論文として十分一般的・重要か。**
2. **理論＋illustrative decision example で投稿し、実データによる検証を別稿にするか。それとも実証1例を今稿に必須と考えるか。**

もし Theoretical Ecology が formal-methods 寄りすぎると判断する場合、Ecological Modelling を即時fallbackとする。
