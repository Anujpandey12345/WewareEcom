import numpy as np
from ..models import Product, Feedback

try:
    from . import similarity
    has_cython = True
except Exception:
    has_cython = False

class Recommender:
    def __init__(self):
        self.product_index = None
        self.sim_matrix = None

    def build_matrix(self):
        fbs = Feedback.objects.select_related('user', 'product').all()
        users = {}
        products = {}
        for fb in fbs:
            uid = fb.user_id
            pid = fb.product_id
            if uid not in users:
                users[uid] = len(users)
            if pid not in products:
                products[pid] = len(products)
        if not products or not users:
            self.product_index = []
            self.sim_matrix = np.array([])
            return
        n_users = len(users)
        n_products = len(products)
        mat = np.zeros((n_products, n_users), dtype=float)
        for fb in fbs:
            i = products[fb.product_id]
            j = users[fb.user_id]
            mat[i, j] = fb.value
        if has_cython:
            try:
                self.sim_matrix = similarity.pairwise_cosine(mat)
            except Exception:
                self.sim_matrix = self._numpy_pairwise(mat)
        else:
            self.sim_matrix = self._numpy_pairwise(mat)
        self.product_index = [0] * len(products)
        for pid, idx in products.items():
            self.product_index[idx] = pid

    def _numpy_pairwise(self, mat):
        norms = np.linalg.norm(mat, axis=1)
        sim = mat.dot(mat.T)
        denom = np.outer(norms, norms)
        denom[denom == 0] = 1e-9
        return sim / denom

    def ensure_built(self):
        if self.sim_matrix is None or self.product_index is None:
            self.build_matrix()

    def recommend_for_user(self, user_id, n=8, seed_product=None):
        self.ensure_built()
        if not len(self.product_index):
            return []
        liked = list(Feedback.objects.filter(user_id=user_id, value=1).values_list('product_id', flat=True))
        if seed_product is not None:
            liked = list(liked) + [seed_product]
        if not liked:
            return list(Product.objects.order_by('-created_at').values_list('id', flat=True)[:n])
        idx_map = {pid: idx for idx, pid in enumerate(self.product_index)}
        scores = np.zeros(len(self.product_index))
        for pid in liked:
            if pid in idx_map:
                scores += self.sim_matrix[idx_map[pid]]
        for pid in liked:
            if pid in idx_map:
                scores[idx_map[pid]] = -1
        top_idx = np.argsort(-scores)[:n]
        result = [self.product_index[i] for i in top_idx if scores[i] > 0]
        if len(result) < n:
            extras = Product.objects.exclude(id__in=result).order_by('-created_at').values_list('id', flat=True)
            for p in extras:
                result.append(p)
                if len(result) >= n:
                    break
        return result[:n]
