# Paper A 指導教員レビュー用 brief

## まず伝えたい結論

Paper A は、当初の「新しい coarsest source-relative repair 定理」を主張する theorem-first 論文から、**構造変化後に既存の生態学的状態分類を管理判断へ再利用してよいかを監査する理論**へ全面的に組み替えた。

現在の中心問いは：

> ある生態系管理で既に使われている状態分類は、種の入れ替わり・相互作用の再配線・生息地変化・新しい介入の導入後にも、管理判断に必要な情報を十分保持しているか。保持していないなら、何を最小限追加して区別・観測すべきか。

## 先行研究精査で撤回した新規性

以下は既知として本文・補足で明示的に引用した。

- 任意の初期分割からの coarsest stable refinement：Paige & Tarjan (1987)
- MDP の coarsest homogeneous refinement：Givan, Dean & Greig (2003)
- MDP state abstraction の体系化：Li, Walsh & Littman (2006)
- source MDP から target MDP への state abstraction transfer：Walsh, Li & Littman (2006)
- 異なる decision process 間の homomorphism：Ravindran & Barto (2003)
- state-and-transition model を用いた targeted monitoring：Jones et al. (2023)
- 生態学的 value of information：Canessa et al. (2015)
- history-preserving / path-sensitive formalism：既存分野として認識

したがって、**generic refinement、generic abstraction transfer、targeted monitoring、VoI、history-sensitive equivalence 自体を新規とは主張しない**。

## 現在主張する貢献

1. **Decision-sufficiency audit**
   - inherited state 内で、target の output、実施可能 action、action 後の successor state が一様かを検査する。
   - 一様なら旧分類をそのまま管理へ使える。

2. **Local obstruction**
   - 旧分類が失敗するとき、「同じ旧stateなのにtarget actionへの応答が異なる」具体的な状態対を返す。

3. **Least exact distinction → monitoring requirement**
   - standard refinement で必要最小限の state split を得る。
   - split された obstruction pair を区別できることを、追加モニタリング変数の要件として読む。

4. **repair の4つの意味を分離**
   - structural state-count defect
   - distribution-sensitive conditional information
   - monitoring realization cost
   - decision regret / downstream VoI
   - 「state が多く増えるほど生態学的影響が大きい」とは主張しない。

5. **route context**
   - 異なる replacement route が同じ terminal state meaning を運ぶなら history は捨てる。
   - incompatible な carried map を運ぶ場合だけ immutable context を残す。

## 植物–送粉者例で何が起きるか

旧分類では Site A と B が同じ pollination state にまとめられている。

pollinator turnover 後、新しい介入が substitute-pollinator response の違いを露出すると、A と B を同じ管理stateとして扱えなくなる。standard refinement はこの exposed fiber だけを split し、追加で観測すべき生態学的差として substitute-response capacity を指す。

さらに、実データを装わない illustrative decision layer として：

- benefit `B=1`
- `c_A=0.20`, `c_B=0.35`
- `p_A=0.25`, `p_B=0.80`

を置くと、旧 pooled state は安い A を選ぶが、repair 後は B を選ぶ。旧判断の one-step regret は `0.40`。一般的な逆転条件は

`p_B - p_A > (c_B - c_A)/B`

であり、この値は実証推定値ではなく sensitivity example と明記している。

## 現在の検証状態

最終 manuscript/supplement revision `bc40b4d28cb997da34c5239b0ce8d207d27e85a3` で：

- CI pass
- transport reproducibility pass
- manuscript build pass
- main 12 pages
- supplement 9 pages
- main abstract 226 words
- 4 figures
- undefined citations 0
- main / supplement 全ページを画像化して目視確認：clip、overlap、missing figure、broken glyph なし

## 教員に本当に判断してほしいこと

ここまでの先行研究・位置づけ・補足整合・再現性は自力で潰した。したがって相談は次の2点に絞れる。

1. **この「生態系管理に使う inherited state representation の監査」という生態学的貢献は、Theoretical Ecology に出す価値があると判断できるか。**
2. **今回の理論＋illustrative decision example までで1本として出し、実データによる検証は別稿にする構成でよいか。**

著者順・所属・Funding・Competing Interests・Author Contributions・対応著者などは、科学的問題ではなく投稿時に確定が必要な事実情報として別途相談する。

## 現在の推奨

新しい定理を増やさず、この版を指導教員レビューへ出す。次に数学を追加するのは、教員または査読者が具体的な論理欠損を指摘した場合だけとする。
